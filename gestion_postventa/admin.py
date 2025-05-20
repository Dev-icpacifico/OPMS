from django.contrib import admin
from .models import (
    RequerimientoPostVenta,
    Recinto, Lugar, Item, Problema,
    Especialidad, Causa, AlcanceResponsabilidad
)


# ✅ Admin para catálogos simples
@admin.register(Recinto)
class RecintoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Problema)
class ProblemaAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    ordering = ('descripcion',)


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Causa)
class CausaAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    ordering = ('descripcion',)


@admin.register(AlcanceResponsabilidad)
class AlcanceResponsabilidadAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    ordering = ('descripcion',)


# ✅ Admin para requerimientos
@admin.register(RequerimientoPostVenta)
class RequerimientoPostVentaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha', 'get_proyecto', 'get_numero_depto', 'get_piso',
        'recinto', 'item', 'especialidad', 'estado',
        'mo', 'materiales', 'subcontrato', 'total'
    )
    list_filter = (
        'fecha', 'estado', 'especialidad',
        'propiedad__condominio', 'propiedad__etapa'
    )
    search_fields = (
        'propiedad__numero_propiedad',
        'recinto__nombre', 'lugar__nombre',
        'item__nombre', 'problema__descripcion',
        'comentario',
    )
    ordering = ('-fecha',)
    date_hierarchy = 'fecha'

    # Métodos personalizados para mostrar datos de la propiedad relacionada
    def get_proyecto(self, obj):
        return obj.propiedad.condominio.alias_condominio
    get_proyecto.short_description = 'Proyecto'

    def get_numero_depto(self, obj):
        return obj.propiedad.numero_propiedad
    get_numero_depto.short_description = 'Depto'

    def get_piso(self, obj):
        return obj.propiedad.piso
    get_piso.short_description = 'Piso'
