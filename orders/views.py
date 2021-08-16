from django.forms import fields
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order, OrderProductItem, OrderFeatureItem, OrderOptionItem
from store.models import Product, Feature, Option, OptionCategory

from .forms import OrderFillForm
from basket.basket import Basket

@login_required
def order(request, order_id) :
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/order.html', {'order' : order})

# @login_required
# def fill_order(request) :
#     basket = Basket(request)
#     if basket.is_empty() :
#         messages.add_message(request, messages.ERROR, 'You have no items in your basket to checkout !!')
#         return redirect('store:product_all')

#     form = OrderFillForm()        
#     if request.method == 'POST' :
#         form = OrderFillForm(request.POST)
#         if form.is_valid() :
#             data = request.POST
#             order = Order.objects.create(user=request.user, fullname=data['fullname'], address1=data['address1'],
#                                 address2=data['address2'], province=data['province'], city=data['city'],
#                                 phone=data['phone'], post_code=data['post_code'])
#             for item in basket :
#                 product = OrderProductItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'])

#                 for feature in item['features'] :
#                     OrderFeatureItem.objects.create(order_product=product, feature=feature, price=feature.price)
#                 for option in item['options'] :
#                     OrderOptionItem.objects.create(order_product=product, option=option, price=option.price)

#             basket.clear()
#             return redirect('orders:order', order.id)

#     return render(request, 'orders/order_fill_form.html', {'form' : form})


## only admin (or anyone that should be able to manipulate orders) must be able to use this function
def product_details(request, pk) :
    if request.method == 'GET' and request.is_ajax() :
        try :
            product = Product.objects.get(pk=pk)
        except :
            return JsonResponse({'error': 'Could not find any result for selected product'}, status=400)
        features = Feature.actives.filter(product=product).order_by('-created')
        data = serializers.serialize('json', list(features), fields=('pk', 'name', 'price'))
        return JsonResponse({'data' : data}, status=200)



