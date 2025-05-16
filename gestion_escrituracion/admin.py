from django.contrib import admin
from .models import Venta, Etapas, VentaEtapa, CampoEtapa, ValoresEtapa
from gestion_contable.admin import PagosInline  # Si mantienes Pagos relacionados a Venta


# Inline: ValoresEtapa dentro de VentaEtapa
class ValoresEtapaInline(admin.TabularInline):
    model = ValoresEtapa
    extra = 1


@admin.register(VentaEtapa)
class VentaEtapaAdmin(admin.ModelAdmin):
    list_display = ('id_venta_etapa', 'id_venta', 'id_etapa', 'fecha_inicio', 'fecha_fin')
    list_filter = ('id_etapa',)
    date_hierarchy = 'fecha_inicio'
    ordering = ('fecha_inicio',)
    inlines = [ValoresEtapaInline]


# Inline: CampoEtapa dentro de Etapas
class CampoEtapaInline(admin.TabularInline):
    model = CampoEtapa
    extra = 1


@admin.register(Etapas)
class EtapasAdmin(admin.ModelAdmin):
    list_display = ('id_etapa', 'alias_etapa', 'nombre_etapa')
    search_fields = ('nombre_etapa', 'alias_etapa')
    ordering = ('id_etapa',)
    inlines = [CampoEtapaInline]


# Inline: VentaEtapa y Pagos dentro de Venta
class VentaEtapaInline(admin.TabularInline):
    model = VentaEtapa
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id_venta', 'id_propiedad', 'id_cliente', 'estado_venta','tipo_venta',
        'fecha_venta', 'fecha_promesa', 'ejecutivo',
        'bono_pie', 'uf_por_m2', 'ggoo'
    )
    list_filter = ('fecha_venta', 'estado_venta', 'ejecutivo', 'tipo_venta')
    search_fields = (
        'id_propiedad__numero_propiedad',
        'id_cliente__rut_cliente',
        'id_cliente__nombres_cliente',
        'id_cliente__apellidos_cliente',
        'ejecutivo',
        'tipo_venta'
    )
    ordering = ('-fecha_venta',)
    date_hierarchy = 'fecha_venta'
    inlines = [VentaEtapaInline, PagosInline]
