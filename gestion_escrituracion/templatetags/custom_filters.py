from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key)

@register.filter
def get_valor(queryset, campo_id):
    # Busca en el queryset de ValoresEtapa el que tenga id_campo_etapa igual al buscado
    for v in queryset:
        if v.id_campo_etapa.id_campo_etapa == campo_id:
            return v.valor_campo
    return ''

from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key)

@register.filter
def get_valor(queryset, campo_id):
    for v in queryset:
        if v.id_campo_etapa.id_campo_etapa == campo_id:
            return v.valor_campo
    return ''
