from django import forms
from django.utils.translation import gettext_lazy as _


class BulkAdd(forms.Form) :
    file = forms.FileField()

    def clean_file(self) :
        file = self.cleaned_data['file']
        content_type = file.content_type
        if not content_type == 'application/json' :
            raise forms.ValidationError(_('Json file is allowed only'))
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)