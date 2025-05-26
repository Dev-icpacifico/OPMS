from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        'razon_social',
        'rut_empresa',
        'gerente_ventas',
        'jefe_operaciones',
        'banco_alzante',
        'notaria',
    )
    search_fields = (
        'razon_social',
        'rut_empresa',
        'gerente_ventas',
        'jefe_operaciones',
    )
    list_filter = ('banco_alzante', 'notaria')

    fieldsets = (
        ('Identificación', {
            'fields': ('razon_social', 'rut_empresa')
        }),
        ('Representantes', {
            'fields': ('gerente_ventas', 'jefe_operaciones')
        }),
        ('Notaría y Bancos', {
            'fields': ('notaria', 'banco_alzante')
        }),
        ('Datos de Transferencia', {
            'fields': ('banco_transf', 'tipo_cuenta_transf', 'num_cuenta_transf', 'correo_transf')
        }),
    )
