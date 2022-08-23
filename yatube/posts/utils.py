from django.core.paginator import Paginator


def custom_paginator(request, list_obj, post_per_page):
    paginator = Paginator(list_obj, post_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
