from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ventas/', ListaVentasView.as_view(), name='lista_ventas'),
    # El endpoint para modificar etapas lo haremos luego:
    path('ventas/<int:venta_id>/etapas/', EtapasVentaView.as_view(), name='editar_etapas'),
    path('informe_pagos/<int:id_venta>/', informe_pagos_venta, name='informe_pagos'),
    # path('informe_pagos_print/<int:id_venta>/', login_required(informe_pagos_venta_print), name='informe_pagos_print'),
    path('pagos_invoice_pdf/<int:id_venta>/', login_required(PagosInvoicePdf.as_view()), name='pagos_invoice_pdf'),

    path('fpm_venta/<int:id_venta>/', login_required(fpm_venta), name='fpm_venta'),
    path('fpm_venta_print/<int:id_venta>/', login_required(Fpm_VentaPdf.as_view()), name='fpm_venta_print'),

]
