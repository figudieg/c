from rest_framework import viewsets
from .models import *
from .serializers import *

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.select_related('pais_origen').all()
    serializer_class = MarcaSerializer

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.select_related('marca', 'tipo').all()
    serializer_class = ModeloSerializer

class VersionTrimViewSet(viewsets.ModelViewSet):
    queryset = VersionTrim.objects.select_related('modelo__marca').all()
    serializer_class = VersionTrimSerializer

class EquipamientoBaseViewSet(viewsets.ModelViewSet):
    queryset = EquipamientoBase.objects.all()
    serializer_class = EquipamientoBaseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        version_id = self.request.query_params.get('version')
        if version_id:
            queryset = queryset.filter(version_id=version_id)
        return queryset

class VehiculoNuevoViewSet(viewsets.ModelViewSet):
    queryset = VehiculoNuevo.objects.select_related('version', 'version__modelo')\
                                   .prefetch_related('version__equipamiento').all()
    serializer_class = VehiculoNuevoSerializer
    
    serializer_class = VehiculoNuevoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        vin = self.request.query_params.get('vin')
        if vin:
            queryset = queryset.filter(vin__icontains=vin)
        return queryset