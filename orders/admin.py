from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path
from django.core import serializers
from django.http import JsonResponse

import json

from .models import Order, OrderProductItem, OrderFeatureItem, OrderOptionItem
from .forms import ProductAddToOrderAdmin

from store.models import Feature, Product


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin) :
    change_form_template = 'admin/order/change_form.html'

    list_display = ('user', 'id', 'city', 'get_total_cost', 'paid', )
    list_filter = ('paid', )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('order_detail/<int:pk>/', self.view_order_details, name='order_details'),
            path('change_item/', self.change_item, name='change_item'),
        ]
        return my_urls + urls

    def view_order_details(self, request, pk):
        products = OrderProductItem.objects.filter(order_id=pk)
        context = dict(
            self.admin_site.each_context(request),
            form = ProductAddToOrderAdmin(),
            products = products,
        )
        
        if request.GET.get('product-id') :
            opi = request.GET.get('product-id')
            order_feature_items = OrderFeatureItem.objects.filter(order_product_id=opi)
            order_option_items = OrderOptionItem.objects.filter(order_product_id=opi)

            context['has_details'] = True
            context['details'] = {'features' : order_feature_items, 'options' : order_option_items}

            product = get_object_or_404(OrderProductItem, pk=opi).product
            features = Feature.actives.filter(product=product)
            option_titles = product.titles.all()
            options = {}
            for title in option_titles :
                options[title.name] = title.options.all()

            context['updates'] = {'features' : features, 'options_details' : options.items()}

        return TemplateResponse(request, "admin/order/manage_order.html", context)

    def change_item(self, request) :
        
        if request.is_ajax() :

            if request.method == 'DELETE' :
                body = json.loads(request.body.decode("utf-8"))
                try :
                    opi = int(body['product_id'])
                except :
                    return JsonResponse({'error' : 'Something is wrong'}, status=400)

                OrderProductItem.objects.filter(pk=opi).delete()

                return JsonResponse({'info': 'Product removed from order'}, status=200)

            if request.method == 'PUT' :
                body = json.loads(request.body.decode("utf-8"))
                try :
                    opi = int(body['product_id'])
                    qty = int(body['productqty'])
                except :
                    return JsonResponse({'error' : 'Something is wrong'}, status=400)

                item = get_object_or_404(OrderProductItem, pk=opi)
                item.quantity = qty
                item.save()

                return JsonResponse({'item_cost': f'{item.get_cost()}'}, status=200)

            if request.method == 'GET' :
                products = Product.products.all()
                serialized_products = serializers.serialize('json', products, fields=('title', 'price', ))

                return JsonResponse({'serialized_products': serialized_products}, status=200)

