from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import gettext_lazy as _


from .models import DeliveryOptions, PaymentSelection
from orders.forms import OrderFillForm
from orders.models import Order, OrderProductItem, OrderOptionItem, OrderFeatureItem

from basket.basket import Basket

import json

@login_required
def deliverychoices(request):
    basket = Basket(request)

    if basket.is_empty():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST' and request.is_ajax() :
        delivery_option = json.loads(request.body.decode("utf-8"))['delivery_id']
        delivery_type = get_object_or_404(DeliveryOptions, id=delivery_option)

        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {"delivery_id": delivery_type.id, }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price},
                                status=201)
        return response

    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})

@login_required
def fill_order(request) :
    # basket = Basket(request)

    # if basket.is_empty() :
    #     messages.add_message(request, messages.ERROR, 'You have no items in your basket to checkout !!')
    #     return redirect('store:product_all')

    if "purchase" not in request.session:
        messages.error(request, _("Please select delivery option"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    if request.method == 'GET' :
        session = request.session
        initial = {}
        if "order_data" in request.session :
            initial = session['order_data']

        form = OrderFillForm(initial=initial)   


    if request.method == 'POST' :
        # form = OrderFillForm(request.POST, instance=request.user) ##wrong
        form = OrderFillForm(request.POST)
        if form.is_valid() :
            data = request.POST
            order_data = {'fullname':data['fullname'], 'address':data['address'],
                    'province':data['province'], 'city':data['city'], 'phone':data['phone'],
                    'post_code':data['post_code'], 'delivery_instructions':data['delivery_instructions'], }

            session = request.session
            if "order_data" not in request.session:
                session["order_data"] = order_data
            else:
                session["order_data"] = order_data
                session.modified = True
            return redirect('checkout:payment_selection')



    #         order = Order.objects.create(user=request.user, fullname=data['fullname'], address1=data['address1'],
    #                             address2=data['address2'], province=data['province'], city=data['city'],
    #                             phone=data['phone'], post_code=data['post_code'])
    #         for item in basket :
    #             product = OrderProductItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'])

    #             for feature in item['features'] :
    #                 OrderFeatureItem.objects.create(order_product=product, feature=feature, price=feature.price)
    #             for option in item['options'] :
    #                 OrderOptionItem.objects.create(order_product=product, option=option, price=option.price)

    #         basket.clear()
    #         return redirect('orders:order', order.id)

    return render(request, 'orders/order_fill_form.html', {'form' : form})


@login_required
def payment_select(request) :

    if "order_data" not in request.session:
        messages.error(request, _("Please fill order page first"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    payments = PaymentSelection.objects.filter(is_active=True)
    return render(request, "checkout/payment_choices.html", {"payments": payments})