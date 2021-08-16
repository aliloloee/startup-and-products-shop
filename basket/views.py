from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import json
from store.models import Product, Feature, Option
from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.method == 'POST' and request.is_ajax() :
        body = json.loads(request.body.decode("utf-8"))
        try :
            product_id = int(body['productid'])
            feature_ids = body['featureids']
            option_ids = body['optionids']
            product_qty = int(body['productqty'])
        except :
            return JsonResponse({'error' : 'Something is wrong'}, status=400)

        product = get_object_or_404(Product, id=product_id)
        features = []
        for feature_id in feature_ids :
            f = get_object_or_404(Feature, id=feature_id)
            features.append(f)

        options = []
        for option_id in option_ids :
            o = get_object_or_404(Option, id=option_id)
            options.append(o)

        # basket.add(product=product,features=features, qty=product_qty)
        basket.add(product=product, features=features, options=options, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty}, status=201)
        return response

def basket_update(request):
    basket = Basket(request)
    if request.method == 'PUT' and request.is_ajax() :
        body = json.loads(request.body.decode("utf-8"))
        try :
            product_id = int(body['productid'])
            product_qty = int(body['productqty'])
            feature_ids = body['featureids']
            option_ids = body['optionids']
        except :
            return JsonResponse({'error' : 'Something is wrong'}, status=400)

        basket.update(product=product_id, qty=product_qty, features=feature_ids, options=option_ids)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal}, status=200)
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.method == 'DELETE' and request.is_ajax() :
        body = json.loads(request.body.decode("utf-8"))
        try :
            product_id = int(body['productid'])
            feature_ids = body['featureids']
            option_ids = body['optionids']
        except :
            return JsonResponse({'error' : 'Something is wrong'}, status=400)

        basket.delete(product=product_id, features=feature_ids, options=option_ids)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal}, status=200)
        return response


