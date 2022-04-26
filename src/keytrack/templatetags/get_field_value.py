from django import template

register = template.Library()

@register.simple_tag
def get_field_value(obj, fieldname):
	return getattr(obj, fieldname)
