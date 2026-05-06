from rest_framework import serializers
from .models import OrdenVenta


class OrdenVentaCreateSerializer(serializers.Serializer):
    """Recibe los campos tal como los envía el frontend (carr)."""
    reference_number = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    # Estos campos vienen del front, pero NO se guardan en OrdenVenta
    # porque la tabla de Dayrom no los tiene.
    cliente_id = serializers.IntegerField() 
    vehiculo_id = serializers.IntegerField()

    def validate_reference_number(self, value):
        if OrdenVenta.objects.filter(referencia=value).exists():
            raise serializers.ValidationError('Ya existe una orden con este número de referencia')
        return value

    def create(self, validated_data):
        # SOLO guardamos lo que el modelo OrdenVenta permite
        return OrdenVenta.objects.create(
            vendedor=self.context['request'].user,
            cliente_id=validated_data['cliente_id'],
            vehiculo_id=validated_data['vehiculo_id'],
            referencia=validated_data['reference_number'],
            precio=validated_data['price'],
            estado='Pendiente'
        )

class OrdenVentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre_completo')
    # TRAEMOS LOS DATOS DEL CLIENTE DESDE LA RELACIÓN
    cliente_email = serializers.ReadOnlyField(source='cliente.correo') 
    cliente_telefono = serializers.ReadOnlyField(source='cliente.telefono_1')
    vendedor_nombre = serializers.SerializerMethodField()
    vin_vehiculo = serializers.ReadOnlyField(source='vehiculo.vin')
    color_vehiculo = serializers.ReadOnlyField(source='vehiculo.color_exterior')
    modelo_vehiculo = serializers.ReadOnlyField(source='vehiculo.version.nombre') 

    class Meta:
        model = OrdenVenta
        fields = [
            'id', 'referencia', 'precio', 'estado', 'created_at',
            'cliente_nombre', 'cliente_email', 'cliente_telefono', # AGREGADOS
            'vendedor_nombre', 'vin_vehiculo', 'color_vehiculo', 'modelo_vehiculo'
        ]

    def get_vendedor_nombre(self, obj):
        # Concatenamos nombre y apellido del vendedor si existen
        nombre = f"{obj.vendedor.first_name} {obj.vendedor.last_name}".strip()
        return nombre if nombre else obj.vendedor.username
