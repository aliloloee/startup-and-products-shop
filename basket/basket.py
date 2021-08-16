from django.shortcuts import get_object_or_404

from decimal import Decimal
from store.models import Product, Feature, Option
from checkout.models import DeliveryOptions


class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def analyze_pre_order_id(self, pre_order_id) :
        temp = pre_order_id.split('+')
        product_id = temp[0]
        feature_ids = temp[1].split(',')
        option_ids = temp[2].split(',')
        return (product_id, feature_ids, option_ids)

    def analyze_features(self, features=[]) :
        f_ids = ''
        f_total_price = 0
        f_list_ids = []
        for feature in features :
            f_list_ids.append(feature.id)
            f_total_price += feature.price

        f_list_ids.sort()
        for id_ in f_list_ids :
            f_ids += f'{id_},'
        f_ids = f_ids[:-1]

        return (f_ids, f_total_price)

    def add(self, product, features=[], options=[], qty=0):

        features_ids , features_total_price = self.analyze_features(features)
        options_ids , options_total_price = self.analyze_features(options)
        pre_order_id = f'{product.id}+{features_ids}+{options_ids}'

        if pre_order_id in self.basket:
            self.basket[pre_order_id]['qty'] = qty
        else:
            product_price = product.discount_price if product.discount_price else product.price
            self.basket[pre_order_id] = {'price': str(product_price + features_total_price + options_total_price), 'qty': qty}

        self.save()

    def __iter__(self):
        basket = self.basket.copy()
        pre_order_ids = self.basket.keys()
        for pre_order_id in pre_order_ids :
            product_id , feature_ids , option_ids = self.analyze_pre_order_id(pre_order_id)
            basket[pre_order_id]['product'] = Product.products.get(pk=product_id)
            try :
                basket[pre_order_id]['features'] = Feature.objects.filter(id__in=feature_ids)
            except :
                basket[pre_order_id]['features'] = []

            try :
                basket[pre_order_id]['options'] = Option.objects.filter(id__in=option_ids)
            except :
                basket[pre_order_id]['options'] = []

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def basket_update_delivery(self, deliveryprice=0):
        subtotal = self.get_total_price()
        total = subtotal + Decimal(deliveryprice)
        return total

    def get_delivery_price(self):
        newprice = 0.00
        if "purchase" in self.session:
            newprice = get_object_or_404(DeliveryOptions, 
                                        id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_and_delivery_price(self):
        newprice = 0.00
        subtotal = self.get_total_price()

        if "purchase" in self.session:
            newprice = get_object_or_404(DeliveryOptions, 
                                        id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def get_delivery_option(self) :
        if "purchase" in self.session:
            return self.session["purchase"]["delivery_id"]
        return None

    def __build_pre_order_id(self, product, features=[], options=[]) :
        features.sort()
        options.sort()
        temp1 = ''
        for feature in features :
            temp1 += f'{feature},'
        temp1 = temp1[:-1]

        temp2 = ''
        for option in options :
            temp2 += f'{option},'
        temp2 = temp2[:-1]
        return f'{product}+{temp1}+{temp2}'

    def update(self, product, qty, features=[], options=[]):
        pre_order_id = self.__build_pre_order_id(product, features, options)

        if pre_order_id in self.basket:
            self.basket[pre_order_id]['qty'] = qty
        self.save()

    def delete(self, product, features=[], options=[]):
        pre_order_id = self.__build_pre_order_id(product, features, options)

        if pre_order_id in self.basket:
            del self.basket[pre_order_id]
            self.save()

    def is_empty(self) :
        if self.basket == {} :
            return True
        else :
            return False

    def save(self):
        self.session.modified = True

    def clear(self) :
        del self.session['skey']
        del self.session["purchase"]
        ## 'order_data key must also be deleted from session
        self.save()