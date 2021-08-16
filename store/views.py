from customUser.models import User
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.core.cache.utils import make_template_fragment_key as mtfk
from django.utils.translation import get_language
from django.conf import settings

from persian_tools import phone_number
from .models import Category, Product, Feature, Option, ProductImage
from BANPars.redis_conf import redis

# For pre-order
from preorder.forms import PreOrderForm
from preorder.models import PreOrder
from django.http import HttpResponseRedirect
from django.contrib import messages



def product_all(request):

    prefix=settings.CACHES['default']['KEY_PREFIX']
    db_number = settings.CACHE_DB_NUMBER

    context = {}
    lang = get_language()
    model_list = [Product, ]

    for model in model_list :

        base_key =  mtfk(f'{model.__name__.lower()}', [lang, ])
        key = f'{prefix}:{db_number}:{base_key}'

        if not redis.exists(key) :
            context[f'{model.__name__.lower()}s'] = model.objects.all()

    return render(request, 'store/home.html', context)

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_products.html', {'category': category, 'products': products})

def product_detail(request, slug):

    # Preorder form submit
    if request.method == 'POST' :
        product = get_object_or_404(Product, slug=slug)
        pre_order = PreOrder(user=request.user, product=product)
        form = PreOrderForm(data=request.POST, instance=pre_order)
        if form.is_valid() :
            form.save()
            messages.success(request, _('Pre-Order was set, we will call you as soon as possible.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else :
            messages.error(request, _('Something went wrong, try again.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # end

    product = get_object_or_404(Product, slug=slug)
    features = Feature.actives.filter(product=product)
    option_titles = product.titles.all()
    options = {}
    for title in option_titles :
        options[title.name] = title.options.all()

    context = {'product': product, 'features' : features, 'options_details' : options.items()}

    prefix=settings.CACHES['default']['KEY_PREFIX']
    db_number = settings.CACHE_DB_NUMBER
    lang = get_language()
    base_key =  mtfk(f'{ProductImage.__name__.lower()}', [lang, product.pk, ])
    key = f'{prefix}:{db_number}:{base_key}'
    if not redis.exists(key) :
        context['images'] = product.product_image.all()

    # Preorder settings
    form = PreOrderForm(initial={'user':request.user.pk, 'product':product.pk, 'phone_number':request.user.username})
    context['form'] = form
    # end
    return render(request, 'store/single.html', context)

@login_required
def toggle_feature(request, pk) :
    if request.method == 'GET' and request.is_ajax() :
        try :
            price = Feature.actives.get(pk=pk).price
        except :
            return JsonResponse({'error': 'Something went wrong'}, status=400)

        response = JsonResponse({'price':price}, status=200)
        return response

@login_required
def toggle_option(request, pk) :
    if request.method == 'GET' and request.is_ajax() :
        try :
            price = Option.objects.get(pk=pk).price
        except :
            return JsonResponse({'error': 'Something went wrong'}, status=400)

        response = JsonResponse({'price':price}, status=200)
        return response

