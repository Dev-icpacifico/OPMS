# Create your views here.
import os
from unittest.mock import right

from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.sites import site
from xhtml2pdf import pisa
from OPMS import settings
from gestion_propiedad.models import Propiedade
from .models import Venta, VentaEtapa, CampoEtapa, ValoresEtapa
from gestion_contable.models import Pagos, ValorUf
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, redirect


class ListaVentasView(TemplateView):
    template_name = 'ventas/listado_ventas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(site.each_context(self.request))
        context['ventas'] = Venta.objects.select_related('id_cliente', 'id_propiedad').filter(estado_venta="Otro_1")
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


from django.shortcuts import render


def test_datatables(request):
    return render(request, 'ventas/test_datatable.html')


from django.db.models import Sum


def informe_pagos_venta(request, id_venta):
    datos = Pagos.objects.filter(id_venta=id_venta)
    datos_venta = Venta.objects.filter(id_venta=id_venta)

    total_pagado = datos.aggregate(total=Sum('monto_pago'))['total'] or 0
    total_pagado_uf = datos.filter(estado_pago="Contabilizado") \
                          .aggregate(total=Sum('uf_pago'))['total'] or 0

    # ✅ Total pagado en categoría "Detalle Pie"
    total_detalle_pie = datos.filter(id_categoria_pago__nombre_categoria_pago="Detalle Pie") \
                            .aggregate(total=Sum('uf_pago'))['total'] or 0
    # Obtener valor UF por cada pago
    valores_uf_por_pago = {}
    for pago in datos:
        if pago.estado_pago == "Contabilizado":
            try:
                valor_uf = ValorUf.objects.get(fecha_registro=pago.fecha_real_pago)
                valores_uf_por_pago[pago.id_pago] = valor_uf.valor_uf
            except ValorUf.DoesNotExist:
                valores_uf_por_pago[pago.id_pago] = None
        else:
            valores_uf_por_pago[pago.id_pago] = None

    # ✅ Extraer el valor inicial de la propiedad (asumiendo 1 resultado)
    valor_inicial_propiedad = None
    if datos_venta.exists():
        valor_inicial_propiedad = datos_venta[0].id_propiedad.valor_inicial_propiedad
        bono_pie = datos_venta[0].bono_pie
        precio_final = datos_venta[0].precio_venta
        credito_hipotecario = datos_venta[0].credito_hipotecario
        total = valor_inicial_propiedad - bono_pie
        saldo_pie = valor_inicial_propiedad - bono_pie - credito_hipotecario - total_detalle_pie

    context = {
        'datos': datos,
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        'total_pagado': total_pagado,
        'total_pagado_uf': total_pagado_uf,
        'valor_inicial_propiedad': valor_inicial_propiedad,
        'bono_pie': bono_pie,
        'precio_final': precio_final,
        'credito_hipotecario': credito_hipotecario,
        'total': total,
        'saldo_pie': saldo_pie,
        'pie_cancelado': total_detalle_pie,
        'valores_uf_por_pago': valores_uf_por_pago,
        **site.each_context(request),
    }
    print(total_pagado)

    return render(request, 'documentos/informe_pagos.html', context)


class PagosInvoicePdf(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            id_venta = self.kwargs['id_venta']
            datos = Pagos.objects.filter(id_venta=id_venta)
            datos_venta = Venta.objects.filter(id_venta=id_venta)

            # Totales
            total_pagado = datos.aggregate(total=Sum('monto_pago'))['total'] or 0
            total_pagado_uf = datos.filter(estado_pago="Contabilizado") \
                                   .aggregate(total=Sum('uf_pago'))['total'] or 0

            total_detalle_pie = datos.filter(id_categoria_pago__nombre_categoria_pago="Detalle Pie") \
                                     .aggregate(total=Sum('uf_pago'))['total'] or 0

            # Valores UF por fecha contable
            valores_uf_por_pago = {}
            for pago in datos:
                if pago.estado_pago == "Contabilizado":
                    try:
                        valor_uf = ValorUf.objects.get(fecha_registro=pago.fecha_real_pago)
                        valores_uf_por_pago[pago.id_pago] = valor_uf.valor_uf
                    except ValorUf.DoesNotExist:
                        valores_uf_por_pago[pago.id_pago] = None
                else:
                    valores_uf_por_pago[pago.id_pago] = None

            # Información de la propiedad
            valor_inicial_propiedad = bono_pie = precio_final = credito_hipotecario = total = saldo_pie = None

            if datos_venta.exists():
                venta = datos_venta[0]
                valor_inicial_propiedad = venta.id_propiedad.valor_inicial_propiedad
                bono_pie = venta.bono_pie
                precio_final = venta.precio_venta
                credito_hipotecario = venta.credito_hipotecario
                total = valor_inicial_propiedad - bono_pie
                saldo_pie = valor_inicial_propiedad - bono_pie - credito_hipotecario - total_detalle_pie

            context = {
                'datos': datos,
                'id_venta': id_venta,
                'datos_venta': datos_venta,
                'total_pagado': total_pagado,
                'total_pagado_uf': total_pagado_uf,
                'valor_inicial_propiedad': valor_inicial_propiedad,
                'bono_pie': bono_pie,
                'precio_final': precio_final,
                'credito_hipotecario': credito_hipotecario,
                'total': total,
                'saldo_pie': saldo_pie,
                'pie_cancelado': total_detalle_pie,
                'valores_uf_por_pago': valores_uf_por_pago,
                'icon': 'static/assets/img/illustrations/logo-horizontal.gif',
            }

            template = get_template('documentos/informe_pagos_pdf.html')
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)

            if pisa_status.err:
                raise Exception("Error al generar PDF con xhtml2pdf")

            return response

        except Exception as e:
            print("❌ Error generando PDF:", e)
            messages.error(request, "Ocurrió un error al generar el PDF.")
            return redirect('lista_ventas')

def fpm_venta(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO

    datos_venta = Venta.objects.filter(id_venta=id_venta)

    context = {
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        **site.each_context(request),
    }

    return render(request, 'documentos/carta_fpm.html', context)


class Fpm_VentaPdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            datos = Pagos.objects.filter(id_venta=self.kwargs['id_venta'])
            datos_venta = Venta.objects.filter(id_venta=self.kwargs['id_venta'])

            template = get_template('documentos/carta_fpm_pdf.html')
            context = {'datos': datos, 'id_venta': self.kwargs['id_venta'], 'datos_venta': datos_venta,
                       'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')

def entrega_documentos_venta(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO
    datos = Pagos.objects.filter(id_venta=id_venta)
    datos_venta = Venta.objects.filter(id_venta=id_venta)

    context = {
        'datos': datos,
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        **site.each_context(request),
    }

    return render(request, 'documentos/memo_entrega_documentos.html', context)



class EntregaDocumentoPdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            datos = Pagos.objects.filter(id_venta=self.kwargs['id_venta'])
            datos_venta = Venta.objects.filter(id_venta=self.kwargs['id_venta'])

            template = get_template('documentos/memo_entrega_documentos_pdf.html')
            context = {'datos': datos, 'id_venta': self.kwargs['id_venta'], 'datos_venta': datos_venta,
                       'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')

def carta_cierre_negocios_venta(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO
    datos_venta = Venta.objects.filter(id_venta=id_venta)
    datos_cierre_negocio = Pagos.objects.filter(id_venta=id_venta,
                                               id_categoria_pago__nombre_categoria_pago="Cierre Negocio")
    # Datos de Detalle Pie
    datos_detalle_pie = Pagos.objects.filter(id_venta=id_venta, id_categoria_pago__nombre_categoria_pago="Detalle Pie")

    context = {
        'datos_detalle_pie': datos_detalle_pie,
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        **site.each_context(request),
    }

    return render(request, 'documentos/carta_cierre_negocio.html', context)


class CierreNegociopdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            # Datos de cierre de negocio
            datos_cierre_negocio = Pagos.objects.filter(id_venta=self.kwargs['id_venta'],
                                                       id_categoria_pago__nombre_categoria_pago="Cierre Negocio")
            # Datos de Detalle Pie
            datos_detalle_pie = Pagos.objects.filter(id_venta=self.kwargs['id_venta'], id_categoria_pago__nombre_categoria_pago="Detalle Pie")

            datos_venta = Venta.objects.filter(id_venta=self.kwargs['id_venta'])
            template = get_template('documentos/carta_cierre_negocio_pdf.html')
            context = {'datos_cierre_negocio': datos_cierre_negocio, 'datos_detalle_pie': datos_detalle_pie,
                       'id_venta': self.kwargs['id_venta'], 'datos_venta': datos_venta,
                       'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')

