from django.db import models
from django.conf import settings


class OrdenVenta(models.Model):
    # Relaciones (Foreign Keys)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='vendedor_id')
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, db_column='cliente_id')


    referencia = models.CharField(max_length=100, unique=True, db_column='codigo_orden')
    precio = models.DecimalField(max_digits=12, decimal_places=2, db_column='precio_final_venta')
    estado = models.CharField(max_length=20, default='Pendiente', db_column='estado_orden')
    created_at = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')


    modelo_vehiculo = models.CharField(max_length=100)
    year_vehiculo = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=50)
    notas = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'orden_venta'
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.referencia} - {self.cliente.nombre_completo}"
