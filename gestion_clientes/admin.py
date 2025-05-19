from django.contrib import admin
from .models import Nacionalidade, AreaProfesion, Profesione, Cliente


@admin.register(Nacionalidade)
class NacionalidadeAdmin(admin.ModelAdmin):
    list_display = ('id_nacionalidad', 'nombre_nacionalidad')
    search_fields = ('nombre_nacionalidad',)
    ordering = ('nombre_nacionalidad',)


@admin.register(AreaProfesion)
class AreaProfesionAdmin(admin.ModelAdmin):
    list_display = ('id_area_profesion', 'nombre_area_profesion')
    search_fields = ('nombre_area_profesion',)
    ordering = ('nombre_area_profesion',)


@admin.register(Profesione)
class ProfesioneAdmin(admin.ModelAdmin):
    list_display = ('id_profesione', 'nombre_profesione', 'id_area_profesion')
    search_fields = ('nombre_profesione',)
    list_filter = ('id_area_profesion',)
    ordering = ('nombre_profesione',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'rut_cliente', 'nombres_1', 'apellidos_1', 'apellidos_2', 'correo', 'telefono',
        'region', 'genero', 'id_profesion', 'renta'
    )
    search_fields = ('rut_cliente', 'nombres_1', 'apellidos_1', 'correo')
    list_filter = ('genero', 'region', 'id_nacionalidad', 'id_profesion')
    ordering = ('id_cliente',)
