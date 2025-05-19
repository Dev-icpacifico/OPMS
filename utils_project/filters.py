from django.contrib.admin import SimpleListFilter
from gestion_propiedad.models import Condominio

class CondominioFilter(SimpleListFilter):
    title = 'Condominio'
    parameter_name = 'condominio'

    def lookups(self, request, model_admin):
        return [(c.id_condominio, c.nombre_condominio) for c in Condominio.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_propiedad__condominio__id_condominio=self.value())
        return queryset
