from django.urls import path
from .views import OrdenVentaListCreateView, OrdenVentaDetailView

urlpatterns = [
    path('ordenes/', OrdenVentaListCreateView.as_view(), name='ordenes-list-create'),
    path('ordenes/<int:pk>/', OrdenVentaDetailView.as_view(), name='ordenes-detail'),
]
