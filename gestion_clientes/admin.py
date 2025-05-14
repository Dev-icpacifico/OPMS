from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut_cliente', 'nombres_cliente', 'apellidos_cliente', 'correo', 'telefono', 'renta')
    search_fields = ('rut_cliente', 'nombres_cliente', 'apellidos_cliente', 'correo')
    list_filter = ('renta',)
    ordering = ('id_cliente',)
