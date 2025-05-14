from django.contrib import admin
from .models import Bancos, CategoriaPago, FormaPago, Pagos

@admin.register(Bancos)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('id_banco', 'nombre_banco')
    search_fields = ('nombre_banco',)
    ordering = ('nombre_banco',)

@admin.register(CategoriaPago)
class CategoriaPagoAdmin(admin.ModelAdmin):
    list_display = ('id_categoria_pago', 'nombre_categoria_pago')
    search_fields = ('nombre_categoria_pago',)
    ordering = ('id_categoria_pago',)

@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ('id_forma_pago', 'nombre_forma_pago')
    search_fields = ('nombre_forma_pago',)
    ordering = ('id_forma_pago',)

# Este inline se puede usar en Venta si quieres
class PagosInline(admin.TabularInline):
    model = Pagos
    extra = 0

@admin.register(Pagos)
class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'id_pago', 'id_venta', 'id_forma_pago', 'id_categoria_pago',
        'id_banco', 'estado_pago', 'num_documento', 'fecha_real_pago', 'monto_pago'
    )
    list_filter = ('estado_pago', 'id_forma_pago', 'id_categoria_pago', 'id_banco')
    search_fields = ('num_documento', 'observacion_pago')
    ordering = ('-fecha_real_pago',)
    date_hierarchy = 'fecha_real_pago'
