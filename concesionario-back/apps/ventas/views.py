# apps/ventas/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import OrdenVenta
from .serializers import OrdenVentaCreateSerializer, OrdenVentaSerializer, OrdenVentaUpdateSerializer


class OrdenVentaListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtener todas las órdenes de venta"""
        ordenes = OrdenVenta.objects.select_related(
            'cliente', 'vendedor', 'vehiculo__version__modelo__marca'
        ).prefetch_related('transacciones_pago').all()
        
        serializer = OrdenVentaSerializer(ordenes, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'total': ordenes.count()
        })

    @transaction.atomic
    def post(self, request):
        """Crear una nueva orden de venta con su transacción de pago"""
        print("=" * 50)
        print("Datos recibidos del frontend:")
        print(request.data)
        print("=" * 50)
        
        serializer = OrdenVentaCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if not serializer.is_valid():
            print("Errores de validación:")
            print(serializer.errors)
            return Response({
                'success': False,
                'errors': serializer.errors,
                'detail': 'Error de validación en los datos enviados'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            orden = serializer.save()
            
            # Serializar la orden creada
            orden_serializer = OrdenVentaSerializer(orden)
            
            return Response({
                'success': True,
                'data': orden_serializer.data,
                'message': f'Orden #{orden.codigo_orden} creada exitosamente'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error al crear la orden: {str(e)}")
            return Response({
                'success': False,
                'detail': f'Error al crear la orden: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrdenVentaDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_orden(self, pk):
        try:
            return OrdenVenta.objects.select_related(
                'cliente', 'vendedor__user', 'vehiculo__version__modelo__marca'
            ).prefetch_related('transacciones_pago').get(pk=pk)
        except OrdenVenta.DoesNotExist:
            return None

    def get(self, request, pk):
        orden = self._get_orden(pk)
        if not orden:
            return Response({'success': False, 'detail': 'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': OrdenVentaSerializer(orden).data})

    @transaction.atomic
    def patch(self, request, pk):
        orden = self._get_orden(pk)
        if not orden:
            return Response({'success': False, 'detail': 'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrdenVentaUpdateSerializer(orden, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        orden_actualizada = serializer.save()
        return Response({
            'success': True,
            'data': OrdenVentaSerializer(orden_actualizada).data,
            'message': f'Orden #{orden_actualizada.codigo_orden} actualizada exitosamente'
        })