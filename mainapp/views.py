import json
import random

from django.conf import settings
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
# Create your views here.
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.core.cache import cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_hot_product():
    products_list = Product.objects.all().filter(is_active=True)

    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).filter(is_active=True)

    return same_products_list[:3]


def index(request):

    products_list = Product.objects.all().filter(is_active=True).select_related()[:4]

    context = {
        'title': 'Мой магазин',
        'products': products_list,
    }
    return render(request, 'mainapp/index.html', context)


@cache_page(3600)
def products(request, pk=None, page=1):
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().filter(is_active=True)
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).filter(is_active=True)

        from django.core.paginator import Paginator
        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category_item,
        }

        return render(request, "mainapp/products_list.html", context)
    hot_product = get_hot_product()
    context = {
        'links_menu': links_menu,
        'title': 'Товары',
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/contacts.json', encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_menu = get_links_menu()
    context = {
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product.html', context)
