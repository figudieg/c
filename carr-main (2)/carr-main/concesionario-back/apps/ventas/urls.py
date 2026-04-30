from django.urls import path
from .views import OrdenVentaListCreateView

urlpatterns = [
    path('ordenes/', OrdenVentaListCreateView.as_view(), name='ordenes-list-create'),
]
