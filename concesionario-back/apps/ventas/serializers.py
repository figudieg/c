# from rest_framework import serializers
# from .models import OrdenVenta


# class OrdenVentaCreateSerializer(serializers.Serializer):
#     print("Inicializando OrdenVentaCreateSerializer")
#     """Recibe los campos tal como los envía el frontend (carr)."""
#     first_name = serializers.CharField(max_length=150)
#     last_name = serializers.CharField(max_length=150)
#     email = serializers.EmailField()
#     phone = serializers.CharField(max_length=20)
#     reference_number = serializers.CharField(max_length=100)
#     price = serializers.DecimalField(max_digits=12, decimal_places=2)
#     vehicleModel = serializers.CharField(max_length=100)
#     vehicleYear = serializers.IntegerField(required=False, allow_null=True)
#     vehicleColor = serializers.CharField(max_length=50)
#     paymentMethod = serializers.CharField(max_length=50)
#     notes = serializers.CharField(required=False, allow_blank=True, default='')

#     def validate_reference_number(self, value):
#         if OrdenVenta.objects.filter(referencia=value).exists():
#             raise serializers.ValidationError('Ya existe una orden con este número de referencia')
#         return value

#     def create(self, validated_data):
#         print("Creando OrdenVenta con los siguientes datos validados:")
#         return OrdenVenta.objects.create(
#             vendedor=self.context['request'].user,
#             cliente_nombre=f"{validated_data['first_name']} {validated_data['last_name']}",
#             cliente_email=validated_data['email'],
#             cliente_telefono=validated_data['phone'],
#             referencia=validated_data['reference_number'],
#             precio=validated_data['price'],
#             modelo_vehiculo=validated_data['vehicleModel'],
#             year_vehiculo=validated_data.get('vehicleYear'),
#             color=validated_data['vehicleColor'],
#             metodo_pago=validated_data['paymentMethod'],
#             notas=validated_data.get('notes', ''),
#         )


# class OrdenVentaSerializer(serializers.ModelSerializer):
#     print("Inicializando OrdenVentaSerializer")
#     # Información del Cliente y Vendedor
#     cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre_completo')
#     vendedor_nombre = serializers.SerializerMethodField()
    
#     # Información disponible en la tabla vehiculo_nuevo (según tu imagen)
#     vin_vehiculo = serializers.ReadOnlyField(source='vehiculo.vin')
#     color_vehiculo = serializers.ReadOnlyField(source='vehiculo.color_exterior')
#     precio_sugerido = serializers.ReadOnlyField(source='vehiculo.precio_lista_sugerido')
#     estado_vehiculo = serializers.ReadOnlyField(source='vehiculo.estado')

#     class Meta:
#         model = OrdenVenta
#         # Solo ponemos campos que existen en el modelo o definimos arriba
#         fields = [
#             'id', 'referencia', 'precio', 'estado', 'created_at',
#             'cliente_nombre', 'vendedor_nombre', 
#             'vin_vehiculo', 'color_vehiculo', 'precio_sugerido', 'estado_vehiculo'
#         ]

#     def get_vendedor_nombre(self, obj):
#         # Concatenamos nombre y apellido del vendedor si existen
#         nombre = f"{obj.vendedor.first_name} {obj.vendedor.last_name}".strip()
#         return nombre if nombre else obj.vendedor.username
# from apps.media.models import MediaAdjunto  # Ajusta según tu estructura
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from .models import OrdenVenta, TransaccionPago, HistorialEstadosOrden
from apps.clientes.models import Cliente
from apps.vehiculos.models import VehiculoNuevo
# from apps.media.models import MediaAdjunto
from apps.catalogos.models import *

class OrdenVentaCreateSerializer(serializers.Serializer):
    """Serializer para crear una orden de venta completa"""
    
    # Datos del cliente
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone1 = serializers.CharField(max_length=20)
    phone2 = serializers.CharField(max_length=20, required=False, allow_blank=True)
    identificacion = serializers.CharField(max_length=50)
    nacionalidad = serializers.CharField(max_length=50)
    direccion = serializers.CharField(max_length=255)
    estado = serializers.CharField(max_length=100)
    
    # Datos del vehículo
    vehiculo_id = serializers.IntegerField(required=True)  # ID del vehículo seleccionado
    vehicleModel = serializers.CharField(max_length=200)
    vehicleYear = serializers.IntegerField(required=False, allow_null=True)
    vehicleColor = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    # Datos de pago
    moneda = serializers.CharField(max_length=10)
    monto_inicial = serializers.DecimalField(max_digits=12, decimal_places=2)
    tasa_cambio = serializers.DecimalField(max_digits=10, decimal_places=4, required=False, allow_null=True)
    paymentMethod = serializers.CharField(max_length=50)
    entidad_financiera = serializers.CharField(max_length=100, required=False, allow_blank=True)
    reference_number = serializers.CharField(max_length=100)
    fecha_pago = serializers.DateField()
    numero_cuotas = serializers.IntegerField(required=False, allow_null=True)
    numero_cuenta = serializers.CharField(max_length=50, required=False, allow_blank=True)
    ultimos_digitos_tarjeta = serializers.CharField(max_length=4, required=False, allow_blank=True)
    url_comprobante = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    
    # Notas adicionales
    notes = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_reference_number(self, value):
        """Validar que la referencia de pago sea única"""
        if TransaccionPago.objects.filter(referencia=value).exists():
            raise serializers.ValidationError('Ya existe una transacción con este número de referencia')
        return value
    
    def validate_vehiculo_id(self, value):
        """Validar que el vehículo exista y esté disponible"""
        try:
            vehiculo = VehiculoNuevo.objects.get(id=value)
            # Verificar que el vehículo esté disponible (estado = 1 o similar)
            if vehiculo.estado_id != 1:  # Asumiendo que 1 = Disponible
                raise serializers.ValidationError('El vehículo seleccionado no está disponible')
        except VehiculoNuevo.DoesNotExist:
            raise serializers.ValidationError('El vehículo seleccionado no existe')
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        Crear la orden de venta completa:
        1. Crear/Actualizar cliente
        2. Crear orden de venta
        3. Crear transacción de pago
        4. Registrar en historial de estados
        5. Actualizar estado del vehículo
        6. Registrar archivo adjunto si existe
        """
        
        # 1. Crear o actualizar el cliente
        cliente, created = Cliente.objects.get_or_create(
            identificacion=validated_data['identificacion'],
            defaults={
                'nombre_completo': f"{validated_data['first_name']} {validated_data['last_name']}",
                'correo': validated_data['email'],
                'telefono_1': validated_data['phone1'],
                'telefono_2': validated_data.get('phone2', ''),
                'nacionalidad_id': validated_data.get('nacionalidad'),
                'direccion': validated_data['direccion'],
                'estado_id': validated_data.get('estado'),
            }
        )
        
        if not created:
            # Actualizar datos del cliente existente
            cliente.nombre_completo = f"{validated_data['first_name']} {validated_data['last_name']}"
            cliente.correo = validated_data['email']
            cliente.telefono_1 = validated_data['phone1']
            cliente.telefono_2 = validated_data.get('phone2', '')
            cliente.nacionalidad_id = validated_data.get('nacionalidad')
            cliente.direccion = validated_data['direccion']
            cliente.estado_id = validated_data.get('estado')
            cliente.save()
        
        # 2. Obtener el vehículo
        vehiculo = VehiculoNuevo.objects.get(id=validated_data['vehiculo_id'])
        
        # 3. Obtener el vendedor del request
        vendedor = self.context['request'].user.vendedor  # Asumiendo relación OneToOne
        
        # 4. Crear la orden de venta
        orden = OrdenVenta.objects.create(
            codigo_orden=validated_data['reference_number'],
            vehiculo=vehiculo,
            cliente=cliente,
            vendedor=vendedor,
            precio_final_venta=validated_data['price'],
            estado_orden_id=1,  # ID del estado "Pendiente" o "En Proceso"
            fecha_creacion=timezone.now()
        )
        
        # 5. Crear la transacción de pago
        monto_total = validated_data['price']
        monto_inicial = validated_data['monto_inicial']
        monto_restante = monto_total - monto_inicial
        
        # Mapear método de pago a ID (según tu catálogo)
        metodo_pago_map = {
            'efectivo': 1,
            'transferencia': 2,
            'financiamiento': 3,
            'tarjeta_credito': 4,
            'tarjeta_debito': 5,
            'cheque': 6,
            'criptomoneda': 7,
            'otro': 8,
        }
        
        # En el método create del serializer:
        transaccion = TransaccionPago.objects.create(
            orden_venta=orden,
            monto=monto_total,
            monto_inicial=monto_inicial,
            monto_restante=monto_restante,
            moneda=validated_data['moneda'],
            tasa_cambio=validated_data.get('tasa_cambio'),
            metodo_pago=int(validated_data['paymentMethod']),  # Convertir a entero
            referencia=validated_data['reference_number'],
            fecha_pago=validated_data['fecha_pago'],
            estado_pago=CtEstadoPago.objects.get(id=1),
            entidad_financiera_id=validated_data.get('entidad_financiera'),
        )
        
        # 6. Registrar en el historial de estados
        HistorialEstadosOrden.objects.create(
            orden=orden,
            estado_anterior=None,  # No hay estado anterior
            estado_nuevo_id=1,  # Primer estado
            fecha_cambio=timezone.now(),
            responsable=vendedor,
        )
        
        # 7. Actualizar estado del vehículo (ej: a "Vendido" o "Reservado")
        vehiculo.estado_id = 2  # 2 = Reservado
        vehiculo.save()
        
        # 8. Registrar comprobante si existe URL
        # if validated_data.get('url_comprobante'):
        #     MediaAdjunto.objects.create(
        #         tabla_referencia='transaccion_pago',
        #         registro_id=transaccion.id,
        #         tipo_archivo='comprobante_pago',
        #         url_archivo=validated_data['url_comprobante'],
        #         fecha_subida=timezone.now()
        #     )
        
        return orden


class OrdenVentaSerializer(serializers.ModelSerializer):
    """Serializer para listar/detallar órdenes de venta"""
    
    cliente_nombre = serializers.CharField(source='cliente.nombre_completo', read_only=True)
    cliente_email = serializers.CharField(source='cliente.correo', read_only=True)
    cliente_telefono = serializers.CharField(source='cliente.telefono_1', read_only=True)
    vendedor_nombre = serializers.SerializerMethodField()
    
    # Información del vehículo
    vehiculo_vin = serializers.CharField(source='vehiculo.vin', read_only=True)
    vehiculo_color = serializers.CharField(source='vehiculo.color_exterior', read_only=True)
    vehiculo_modelo = serializers.SerializerMethodField()
    
    # Información de pago (desde la transacción)
    transaccion_info = serializers.SerializerMethodField()
    
    class Meta:
        model = OrdenVenta
        fields = [
            'id', 'codigo_orden', 'precio_final_venta', 'fecha_creacion',
            'cliente_nombre', 'cliente_email', 'cliente_telefono',
            'vendedor_nombre', 'vehiculo_vin', 'vehiculo_color', 'vehiculo_modelo',
            'transaccion_info', 'estado_orden'
        ]
    
    def get_vendedor_nombre(self, obj):
        if obj.vendedor and obj.vendedor.user:
            return f"{obj.vendedor.user.first_name} {obj.vendedor.user.last_name}".strip()
        return ''
    
    def get_vehiculo_modelo(self, obj):
        if obj.vehiculo and obj.vehiculo.version:
            version = obj.vehiculo.version
            modelo = version.modelo
            marca = modelo.marca
            return f"{marca.nombre} {modelo.nombre} {version.nombre_version}"
        return ''
    
    def get_transaccion_info(self, obj):
        """Obtener la información de la transacción de pago asociada"""
        try:
            transaccion = obj.transacciones_pago.first()
            if transaccion:
                return {
                    'id': transaccion.id,
                    'monto': str(transaccion.monto),
                    'monto_inicial': str(transaccion.monto_inicial),
                    'monto_restante': str(transaccion.monto_restante),
                    'moneda': transaccion.moneda,
                    'metodo_pago': transaccion.metodo_pago,
                    'referencia': transaccion.referencia,
                    'fecha_pago': transaccion.fecha_pago,
                    'estado_pago': transaccion.estado_pago_id,
                }
        except:
            pass
        return None