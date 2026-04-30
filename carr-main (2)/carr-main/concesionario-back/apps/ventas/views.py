from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import OrdenVenta
from .serializers import OrdenVentaCreateSerializer, OrdenVentaSerializer


class OrdenVentaListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ordenes = OrdenVenta.objects.select_related('vendedor').all()
        serializer = OrdenVentaSerializer(ordenes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrdenVentaCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        orden = serializer.save()
        return Response(
            OrdenVentaSerializer(orden).data,
            status=status.HTTP_201_CREATED
        )
