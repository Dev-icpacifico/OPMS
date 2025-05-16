from django.urls import path
from .views import ListaVentasView, EtapasVentaView

urlpatterns = [
    path('ventas/', ListaVentasView.as_view(), name='lista_ventas'),
    # El endpoint para modificar etapas lo haremos luego:
    path('ventas/<int:venta_id>/etapas/', EtapasVentaView.as_view(), name='editar_etapas'),
]
