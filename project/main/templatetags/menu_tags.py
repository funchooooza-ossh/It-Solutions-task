from django import template
from main.models import Menu
from django.urls import reverse
from django.template.loader import render_to_string




register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']  
    menu = Menu.objects.prefetch_related('items__children').get(name=menu_name)
    return render_to_string('main/menu.html', {'menu': menu, 'request': request})