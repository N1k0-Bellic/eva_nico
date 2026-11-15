from django import template

register = template.Library()


@register.filter
def pesos_chilenos(valor):
    return f"${valor:,.0f}".replace(",", ".")