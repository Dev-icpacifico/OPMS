from django.contrib import admin
from .models import Nacionalidade, AreaProfesion, Profesione, Cliente
from import_export.admin import ImportExportModelAdmin
from import_export import resources

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


# Recurso de importación/exportación
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['rut_cliente']  # Puedes cambiarlo si prefieres usar otro identificador único
        fields = (
            'id_cliente', 'rut_cliente', 'nombres_1', 'nombres_2',
            'apellidos_1', 'apellidos_2', 'correo', 'telefono',
            'genero', 'estado_civil', 'fecha_nacimiento',
            'direccion', 'region', 'ciudad',
            'nivel_educacional', 'renta',
            'id_nacionalidad', 'id_profesion', 'tipo_cliente'
        )

@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ClienteResource
    list_display = (
        'rut_cliente', 'nombres_1', 'apellidos_1', 'apellidos_2', 'correo', 'telefono',
        'region', 'genero', 'id_profesion', 'renta'
    )
    search_fields = ('rut_cliente', 'nombres_1', 'apellidos_1', 'correo')
    list_filter = ('genero', 'region', 'id_nacionalidad', 'id_profesion')
    ordering = ('id_cliente',)
