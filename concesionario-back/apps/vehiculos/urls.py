from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'modelos', ModeloViewSet)
router.register(r'versiones', VersionTrimViewSet)
router.register(r'equipamiento', EquipamientoBaseViewSet)
router.register(r'inventario', VehiculoNuevoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]