from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Propiedade


@admin.register(Propiedade)
class PropiedadeAdmin(admin.ModelAdmin):
    list_display = (
        'id_propiedad', 'estado_propiedad', 'condominio', 'alias_condominio',
        'etapa', 'rol', 'numero_propiedad', 'modelo'
    )
    search_fields = ('alias_condominio', 'rol', 'numero_propiedad', 'modelo')
    list_filter = ('estado_propiedad', 'condominio', 'etapa')
    ordering = ('id_propiedad',)
