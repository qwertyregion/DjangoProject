from django import template
from django.db.models import Count
from sait_app.models import Publisher, Tag

register = template.Library()


@register.simple_tag
def list_menu():
    menu = [
        {'name': 'home', 'url_name': 'sait_app:home'},
        {'name': 'contact', 'url_name': 'sait_app:contact'},
        {'name': 'news', 'url_name': 'sait_app:news'},
        {'name': 'chat', 'url_name': 'sait_app:chat'},
        # {'name': 'register_page', 'url_name': 'users:register'},
    ]
    return menu


@register.inclusion_tag(filename="sait_app/list_publisher.html")
def list_publisher():
    publisher_table = Publisher.objects.annotate(count_author=Count("author")).filter(count_author__gt=0)
    return {'publisher_table': publisher_table, }


@register.inclusion_tag(filename='sait_app/list_tag.html')
def list_tag():
    tag_table = Tag.objects.all().annotate(count_author=Count("author")).filter(count_author__gt=0)
    return {'tag_table': tag_table}


@register.inclusion_tag(filename='sait_app/paginator.html', takes_context=True, )
def inclusion_paginator(context):
    paginator = context['paginator']
    page_obj = context['page_obj']
    return {'paginator': paginator,
            'page_obj': page_obj,
            }
