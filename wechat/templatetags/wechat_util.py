# -*- coding: utf-8 -*-
__author__ = 'sincat'
from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter
def radio_checked(value, item_value):
    if value == item_value:
        return mark_safe('checked value="%s"' % item_value)
    else:
        return mark_safe('value="%s"' % item_value)


