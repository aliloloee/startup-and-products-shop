from django import forms
from django.db.models import fields
from django.utils.translation import gettext_lazy as _

from .models import PreOrder

from persian_tools import phone_number

class PreOrderForm(forms.ModelForm) :

    class Meta :
        model = PreOrder
        fields = ('fullname', 'phone_number', )

    def clean_phone_number(self) :
        number = self.cleaned_data['phone_number']
        if not phone_number.validate(number) :
            raise forms.ValidationError(_('wrong phone number.'))
        return number

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
