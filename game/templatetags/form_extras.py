from django import template

register = template.Library()

@register.filter(name='addattrs')
def addattrs(field, attrs):
    attrs = attrs.split(';')
    for attr in attrs:
        k, v = attr.split(':')
        field.field.widget.attrs[k] = v
    return field