# custom_tags.py
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def absolute_uri(context, relative_url):
    request = context['request']
    return request.build_absolute_uri(relative_url)