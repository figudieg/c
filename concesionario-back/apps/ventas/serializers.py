from rest_framework import serializers
from .models import OrdenVenta


class OrdenVentaCreateSerializer(serializers.Serializer):
    """Recibe los campos tal como los envía el frontend (carr)."""
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    reference_number = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    vehicleModel = serializers.CharField(max_length=100)
    vehicleYear = serializers.IntegerField(required=False, allow_null=True)
    vehicleColor = serializers.CharField(max_length=50)
    paymentMethod = serializers.CharField(max_length=50)
    notes = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_reference_number(self, value):
        if OrdenVenta.objects.filter(referencia=value).exists():
            raise serializers.ValidationError('Ya existe una orden con este número de referencia')
        return value

    def create(self, validated_data):
        return OrdenVenta.objects.create(
            vendedor=self.context['request'].user,
            cliente_nombre=f"{validated_data['first_name']} {validated_data['last_name']}",
            cliente_email=validated_data['email'],
            cliente_telefono=validated_data['phone'],
            referencia=validated_data['reference_number'],
            precio=validated_data['price'],
            modelo_vehiculo=validated_data['vehicleModel'],
            year_vehiculo=validated_data.get('vehicleYear'),
            color=validated_data['vehicleColor'],
            metodo_pago=validated_data['paymentMethod'],
            notas=validated_data.get('notes', ''),
        )


class OrdenVentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre_completo')
    cliente_identificacion = serializers.ReadOnlyField(source='cliente.identificacion')
    vendedor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = OrdenVenta
        fields = [
            'id', 'referencia', 'precio', 'estado', 'created_at',
            'cliente_nombre', 'cliente_identificacion', 'vendedor_nombre',
            'modelo_vehiculo', 'year_vehiculo', 'color', 'metodo_pago', 'notas'
        ]

    def get_vendedor_nombre(self, obj):
        nombre = f"{obj.vendedor.first_name} {obj.vendedor.last_name}".strip()
        return nombre if nombre else obj.vendedor.username
