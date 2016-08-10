# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from copy import copy
from django import template

register = template.Library()


def paginator(context, paginated_object_list, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    page = paginated_object_list.number
    pages = paginated_object_list.paginator.num_pages
    page_numbers = [n for n in \
                    range(page - adjacent_pages, page + adjacent_pages + 1) \
                    if n > 0 and n <= pages]
    return {
            'params': context.get('params'),
            #'hits': context['hits'],
            'results_per_page': paginated_object_list.paginator.per_page,
            'page': page,
            'pages': pages,
            'page_numbers': page_numbers,
            'next': page + 1,
            'previous': page - 1,
            'has_next': paginated_object_list.has_next(),
            'has_previous': paginated_object_list.has_previous(),
            'show_first': 1 not in page_numbers,
            'show_last': pages not in page_numbers,
            'count': paginated_object_list.paginator.count,
            'start_index': paginated_object_list.start_index,
            'end_index': paginated_object_list.end_index

    }

register.inclusion_tag('paginator.html', takes_context=True)(paginator)


@register.filter
def update_page(params, page):
    res = copy((params or {}))
    res['page'] = page
    return res

@register.filter
def update_status(params, value):
    res = copy((params or {}))
    res['status'] = value
    return res

@register.filter
def gen_get_params(params):
    res = []
    for k, v in params.iteritems():
        res.append('%s=%s' % (k, v))

    return '?' + '&'.join(res)

@register.filter
def remove_key(params, key):
    res = copy((params or {}))
    res.pop(key, None)
    return res
