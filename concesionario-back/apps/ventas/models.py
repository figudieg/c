from django.db import models
from django.conf import settings


class OrdenVenta(models.Model):
    # Relaciones exactas del diagrama
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='vendedor_id')
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, db_column='cliente_id')
    vehiculo = models.ForeignKey('vehiculos.VehiculoNuevo', on_delete=models.PROTECT, db_column='vehiculo_id')

    # Campos físicos que veo en tu tabla orden_venta
    referencia = models.CharField(max_length=100, unique=True, db_column='codigo_orden')
    precio = models.DecimalField(max_digits=12, decimal_places=2, db_column='precio_final_venta')
    estado = models.CharField(max_length=20, default='Pendiente', db_column='estado_orden')
    created_at = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        managed = False  # ESTO evita que Django intente crear/borrar tablas
        db_table = 'orden_venta'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"#{self.referencia} - {self.cliente.nombre_completo}"
