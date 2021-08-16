from django import forms
from django.contrib.auth import models
from django.db.models import fields
from django.utils.translation import gettext_lazy as _

from .models import Order
from store.models import Product
from addresses.models import City

from persian_tools import phone_number


class OrderFillForm(forms.ModelForm) :
    # fullname = forms.CharField(label=_('Fullname'), max_length=50)
    # address1 = forms.CharField(label=_('First Address'), max_length=250)
    # address2 = forms.CharField(label=_('Second Address'), max_length=250)
    # description = forms.Textarea(label=_('Description'))
    # province = forms.CharField(label=_('Province'), max_length=50)
    # city = forms.CharField(label=_('City'), max_length=50)
    # phone = forms.CharField(label=_('Phone Number'), max_length=11, help_text='Please provide a valid number in case we needed to cantact you')
    # post_code = forms.CharField(label=_('Post Code'), max_length=20)

    class Meta : 
        model = Order
        fields = ('fullname', 'address', 'delivery_instructions', 'province', 'city', 'phone', 'post_code')

    def clean_address(self) :
        address = self.cleaned_data['address']
        if address == '' :
            raise forms.ValidationError(_('Address can not be blank, Please fill it.'))
        return address

    def clean_province(self) :
        province = self.cleaned_data['province']
        if province == '' :
            raise forms.ValidationError(_('Province can not be blank, Please fill it.'))
        return province

    def clean_city(self) :
        city = self.cleaned_data['city']
        if city == '' :
            raise forms.ValidationError(_('City can not be blank, Please fill it.'))
        return city

    def clean_phone(self) :
        phone = self.cleaned_data['phone']
        if not phone_number.validate(phone) :
            raise forms.ValidationError(_('Phone Number is not correct, Please correct it.'))
        return phone

    def clean_post_code(self) :
        post_code = self.cleaned_data['post_code']
        if post_code == '' or len(post_code) != 10 :
            raise forms.ValidationError(_('Post Code is not correct, Please correct it.'))

    def __init__(self, *args, **kwargs):

        initial = kwargs.get('initial', None)
        if initial  :
            queryset = City.objects.filter(province=initial.get('province') )
        else :
            queryset = City.objects.none()

        super().__init__(*args, **kwargs)
        self.fields['delivery_instructions'].required = False
        self.fields['city'].queryset = queryset


        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = City.objects.filter(province=province_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.province.city_set.all()




class ProductAddToOrderAdmin(forms.Form) :
    order = forms.ModelChoiceField(queryset=Order.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())
