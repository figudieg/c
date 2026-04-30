from django.db import models
from rest_framework import serializers

class CtPais(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_iso = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=255)
    continente = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ct_pais'

    def __str__(self):
        return f"{self.codigo_iso} - {self.nombre}"

class CtTipoModelo(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ct_tipo_modelo'

    def __str__(self):
        return self.tipo

class CtEstadoVehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ct_estado_vehiculo'

    def __str__(self):
        return self.estado

class CtEstadoVenezuela(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ct_estado_venezuela'

    def __str__(self):
        return self.nombre

class CtEntidadFinanciera(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo_identificador = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'ct_entidad_financiera'

    def __str__(self):
        return self.nombre

class CtEstadoOrden(models.Model):
    id = models.AutoField(primary_key=True)
    estado_orden = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'ct_estado_orden'

    def __str__(self):
        return self.estado_orden