from django.db import models
from django.conf import settings


class OrdenVenta(models.Model):
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='vendedor_id'
    )
    cliente_nombre = models.CharField(max_length=255)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20)
    referencia = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    modelo_vehiculo = models.CharField(max_length=100)
    year_vehiculo = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=50)
    notas = models.TextField(blank=True, default='')
    estado = models.CharField(max_length=20, default='Pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orden_venta'
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.referencia} - {self.cliente_nombre}"
