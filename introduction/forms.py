from django import forms
from django.db import models
from django.forms import fields
from django.utils.translation import gettext_lazy as _

from . models import Contact


class ContactForm(forms.ModelForm) :

    class Meta :
        model = Contact
        fields = ('fullname', 'mobile', 'message', )

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs.update({'placeholder' : _('Your Name')})
        self.fields['mobile'].widget.attrs.update({'placeholder' : _('Your Number')})
        self.fields['message'].widget.attrs.update({'placeholder' : _('Your Message')})
