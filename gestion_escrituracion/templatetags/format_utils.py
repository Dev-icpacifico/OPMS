from django import template

register = template.Library()

@register.filter
def uf_format(value):
    try:
        valor = float(value)
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " UF"
    except:
        return "—"

@register.filter
def clp_format(value):
    try:
        value = round(float(value))
        return f"${value:,.0f}".replace(",", ".") + ".-"
    except:
        return "$0.-"
