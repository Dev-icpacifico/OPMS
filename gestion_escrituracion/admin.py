from django.contrib import admin
from django.utils.html import format_html
from utils_project.filters import CondominioFilter
from .models import Venta, Etapas, VentaEtapa, CampoEtapa, ValoresEtapa
from gestion_contable.admin import PagosInline  # Si mantienes Pagos relacionados a Venta
from django.contrib.admin import RelatedOnlyFieldListFilter


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
        'id_venta', 'get_condominio', 'get_etapa', 'get_numero_propiedad', 'id_cliente', 'estado_venta', 'tipo_venta',
        'fecha_venta', 'fecha_promesa', 'ejecutivo','get_precio_ini_propiedad', 'format_pventa','descuento_campagna','format_ufdsctocam',
        'bono_pie', 'aplicacion_bono','uf_por_m2', 'format_ggoo'
    )
    """list_filter = ('fecha_venta', 'estado_venta', 'ejecutivo',
                   'tipo_venta', 'id_propiedad__condominio',
                   'id_propiedad__etapa',
                   )"""
    # list_filter = ('id_propiedad__condominio',  )
    list_filter = (
        'fecha_venta',
        'estado_venta',
        'ejecutivo',
        'tipo_venta',
        CondominioFilter
    )
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

    def get_condominio(self, obj):
        return obj.id_propiedad.condominio.alias_condominio

    get_condominio.short_description = 'Condominio'
    get_condominio.admin_order_field = 'id_propiedad__condominio__alias_condominio'

    def get_etapa(self, obj):
        return obj.id_propiedad.etapa.nombre_etapa

    get_etapa.short_description = 'Etapa'
    get_etapa.admin_order_field = 'id_propiedad__etapa__nombre_etapa'

    def get_numero_propiedad(self, obj):
        return obj.id_propiedad.numero_propiedad

    get_numero_propiedad.short_description = 'N°'
    get_numero_propiedad.admin_order_field = 'id_propiedad__numero_propiedad'

    def get_precio_ini_propiedad(self, obj):
        if obj.id_propiedad.valor_inicial_propiedad is not None:
            return f"UF {obj.id_propiedad.valor_inicial_propiedad:,.0f}".replace(",", ".")
        return "-"

    get_precio_ini_propiedad.short_description = 'P.Ini'
    get_precio_ini_propiedad.admin_order_field = 'valor_inicial_propiedad'


    def format_ggoo(self, obj):
        if obj.ggoo is None:
            return "-"
        return format_html("$ {:,}".format(obj.ggoo).replace(",", "."))

    format_ggoo.short_description = 'GGOO'
    format_ggoo.admin_order_field = 'ggoo'  # 👈 Esto habilita la ordenación por ese campo

    def format_ufdsctocam(self, obj):
        if obj.uf_descuento_campagna is None:
            return "-"
        return format_html("UF {:,}".format(obj.uf_descuento_campagna).replace(",", "."))

    format_ufdsctocam.short_description = 'Dcts Cam'
    format_ufdsctocam.admin_order_field = 'uf_descuento_campagna'

    def format_pventa(self, obj):
        if obj.precio_venta is None:
            return "-"
        return format_html("UF {:,}".format(obj.precio_venta).replace(",", "."))

    format_pventa.short_description = 'P.Venta'
    format_pventa.admin_order_field = 'precio_venta'  # 👈 Esto habilita la ordenación por ese campo