# Create your views here.
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.sites import site
from .models import Venta, VentaEtapa, CampoEtapa, ValoresEtapa

class ListaVentasView(TemplateView):
    template_name = 'ventas/listado_ventas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(site.each_context(self.request))
        context['ventas'] = Venta.objects.select_related('id_cliente', 'id_propiedad')
        return context



class EtapasVentaView(View):
    template_name = 'ventas/editar_etapas.html'

    def get(self, request, venta_id):
        venta = get_object_or_404(Venta, id_venta=venta_id)
        etapas = VentaEtapa.objects.filter(id_venta=venta).select_related('id_etapa')

        campos_etapas = {
            ve.id_etapa.id_etapa: CampoEtapa.objects.filter(id_etapa=ve.id_etapa)
            for ve in etapas
        }

        valores_etapas = {
            ve.id_etapa.id_etapa: list(ValoresEtapa.objects.filter(id_venta_etapa=ve))
            for ve in etapas
        }

        context = {
            'venta': venta,
            'etapas': etapas,
            'campos_etapas': campos_etapas,
            'valores_etapas': valores_etapas,
            'title': f'Editar etapas de la venta #{venta.id_venta}',
            **site.each_context(request),
        }

        return render(request, self.template_name, context)

    def post(self, request, venta_id):
        venta = get_object_or_404(Venta, id_venta=venta_id)
        etapas = VentaEtapa.objects.filter(id_venta=venta).select_related('id_etapa')

        for etapa in etapas:
            campos = CampoEtapa.objects.filter(id_etapa=etapa.id_etapa)
            for campo in campos:
                field_name = f"campo_{campo.id_campo_etapa}"
                valor = request.POST.get(field_name)
                if valor is not None:
                    valor_etapa, created = ValoresEtapa.objects.get_or_create(
                        id_venta_etapa=etapa,
                        id_campo_etapa=campo,
                        defaults={'valor_campo': valor}
                    )
                    if not created:
                        valor_etapa.valor_campo = valor
                        valor_etapa.save()

        messages.success(request, "Los datos fueron guardados correctamente.")
        return redirect('editar_etapas', venta_id=venta.id_venta)