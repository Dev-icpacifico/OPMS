from django.contrib import admin
from .models import (
    Condominio, Etapa, SubEtapa, Torre, Modelo, Propiedade
)
from django.utils.html import format_html
from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html

# Inline: Etapa dentro de Condominio
class EtapaInline(admin.TabularInline):
    model = Etapa
    extra = 1


@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ('id_condominio', 'empresa_vende','nombre_condominio', 'alias_condominio', 'direccion_proyecto', 'fecha_venta_condominio', 'estado_condominio')
    search_fields = ('nombre_condominio', 'alias_condominio', 'direccion_proyecto','empresa_vende')
    list_filter = ('estado_condominio','empresa_vende')
    ordering = ('id_condominio',)
    inlines = [EtapaInline]


# Inline: SubEtapa dentro de Etapa
class SubEtapaInline(admin.TabularInline):
    model = SubEtapa
    extra = 1


# Inline: Torre dentro de Etapa
class TorreInline(admin.TabularInline):
    model = Torre
    extra = 1


@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ('id_etapa_condominio', 'nombre_etapa', 'id_condominio')
    search_fields = ('nombre_etapa',)
    list_filter = ('id_condominio',)
    ordering = ('id_etapa_condominio',)
    inlines = [SubEtapaInline, TorreInline]


@admin.register(SubEtapa)
class SubEtapaAdmin(admin.ModelAdmin):
    list_display = ('id_sub_etapa', 'nombre_sub_etapa', 'etapa')
    list_filter = ('etapa',)
    ordering = ('id_sub_etapa',)


@admin.register(Torre)
class TorreAdmin(admin.ModelAdmin):
    list_display = ('id_torre', 'nombre_torre', 'id_etapa_condominio', 'estado_torre')
    list_filter = ('estado_torre',)
    search_fields = ('nombre_torre',)
    ordering = ('id_torre',)


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('id_modelo', 'nombre_modelo', 'programa_modelo', 'estado_modelo')
    search_fields = ('nombre_modelo',)
    list_filter = ('estado_modelo',)
    ordering = ('id_modelo',)



# Recurso para import-export
class PropiedadeResource(resources.ModelResource):
    class Meta:
        model = Propiedade
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['id_propiedad']  # Puedes cambiar a 'numero_propiedad' si lo prefieres
        fields = (
            'id_propiedad',
            'numero_propiedad', 'condominio', 'etapa', 'torre', 'rol',
            'modelo', 'estado_propiedad', 'ori_propiedad', 'piso',
            'metros_vivienda', 'metros_terraza_propiedad', 'metros_total_propiedad',
            'bono_propiedad', 'prorrateo_propiedad',
            'estacionamiento', 'valor_estacionamiento', 'rol_estacionamiento',
            'bodega', 'valor_bodega', 'rol_bodega', 'm2_bodega',
            'valor_inicial_propiedad', 'valor_final_propiedad', 'valor_cchc', 'fpm',
        )


@admin.register(Propiedade)
class PropiedadeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PropiedadeResource
    list_display = (
        'numero_propiedad', 'condominio', 'etapa',
        'estado_propiedad', 'modelo', 'piso', 'format_vip',
        'format_vfp', 'fpm', 'estacionamiento', 'valor_estacionamiento',
        'bodega', 'valor_bodega',
        'metros_vivienda', 'metros_terraza_propiedad', 'metros_total_propiedad'
    )
    search_fields = ('numero_propiedad', 'rol')
    list_filter = ('estado_propiedad', 'condominio', 'etapa', 'modelo')
    ordering = ('id_propiedad',)

    def format_vip(self, obj):
        if obj.valor_inicial_propiedad is None:
            return "-"
        return format_html("UF {:,}".format(obj.valor_inicial_propiedad).replace(",", "."))

    format_vip.short_description = 'Precio Ini'
    format_vip.admin_order_field = 'valor_inicial_propiedad'

    def format_vfp(self, obj):
        if obj.valor_final_propiedad is None:
            return "-"
        return format_html("UF {:,}".format(obj.valor_final_propiedad).replace(",", "."))

    format_vfp.short_description = 'Precio Fin'
    format_vfp.admin_order_field = 'valor_final_propiedad'



