from django import forms
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext_lazy as _

from customUser.models import User
from .models import Profile

from BANPars.redis_conf import redis

from persian_tools import phone_number
from BANPars.settings import OTP_LENGTH


def has_numbers_and_alphabet(inputString):
    a = any(char.isdigit() for char in inputString)
    b = any(char.isalpha() for char in inputString)
    return (a and b)


class RegistrationForm(forms.Form) :
    username = forms.CharField(label=_('Phone Number'), max_length=11, help_text=_('Required'),
                                error_messages={'required' : _('Phonenumber can not be blank'),
                                                            'invalid': _('Invalid phonenumber')})

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_username(self) :
        username = self.cleaned_data['username']

        if not phone_number.validate(username) :
            raise forms.ValidationError('Phonenumber is not valid')

        r = User.objects.filter(username=username)
        if r.count() :
            raise forms.ValidationError('Username already exists')

        return username

    # Password circumastances = at least 5 char long, including digits and alphabets
    def clean_password1(self) :
        password = self.cleaned_data['password']
        if len(password) < 5 :
            raise forms.ValidationError('Password must be at least 5 characters long')
        if not has_numbers_and_alphabet(password) :
            raise forms.ValidationError('Password must contain digits and alphabets')

        cd = self.cleaned_data
        if cd['password'] != cd['password1'] :
            raise forms.ValidationError('Passwords do not match !!!')

        return cd['password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': _('Username'), })
        self.fields['password'].widget.attrs.update(
            {'placeholder': _('Password'), })
        self.fields['password1'].widget.attrs.update(
            {'placeholder': _('Repeat Password'), })

class VerificationForm(forms.Form) :
    number = forms.CharField(label=_('Phone Number'), max_length=11, help_text=_('Required'),
                            error_messages={'required' : _('Phonenumber can not be blank'),
                                'invalid': _('Invalid Phonenumber')})

    otp = forms.CharField(label=_('Verification Code'), help_text=_('Required'),
                            error_messages={'required' : _('OTP can not be blank'),
                                'invalid': _('Invalid OTP')})

    def clean_number(self) :
        number = self.cleaned_data['number']
        if not phone_number.validate(number) :
            raise forms.ValidationError(_('Wrong Phonenumber'))
        return number

    def clean_otp(self) :
        number = self.cleaned_data['number']
        otp = self.cleaned_data['otp']
        try :
            predefined_otp = redis.get(str(number)).decode('utf-8')
        except :
            raise forms.ValidationError(_('Verification code is expired, press resend'))

        if not otp == predefined_otp :
            raise forms.ValidationError(_('Wrong code, try again'))
        else :
            return otp

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].widget.attrs.update(
            {'placeholder': _('Phone Number'), })
        self.fields['otp'].widget.attrs.update(
            {'placeholder': _('Verification Code'), })

class UserLoginForm(forms.Form) :
    username = forms.CharField(label=_('Username'),
                                help_text=_('Required'),
                                error_messages={'invalid' : _('Username must contain at least 5 characters'), })
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    def clean_username(self) :
        username = self.cleaned_data['username'].lower()
        try :
            r = User.objects.get(username=username)
        except :
            r = None
        if not r :
            raise forms.ValidationError(_('Wrong crendtials'))
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': _('Username'), })
        self.fields['password'].widget.attrs.update(
            {'placeholder': _('Password'), })

class SetNewPasswordForm(forms.Form) :
    password = forms.CharField(label=_('New Password'), widget=forms.PasswordInput)
    password1 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput)

    def clean_password1(self) :
        cd = self.cleaned_data
        if cd['password'] != cd['password1'] :
            raise forms.ValidationError('Passwords do not match !!!')
        password = self.cleaned_data['password']
        if len(password) < 5 :
            raise forms.ValidationError('Password must be at least 5 characters long')
        if not has_numbers_and_alphabet(password) :
            raise forms.ValidationError('Password must contain digits and alphabets')
        return cd['password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder': _('New Password'), })
        self.fields['password1'].widget.attrs.update({'placeholder': _('Repeat New Password'), })

class UserEditForm (forms.ModelForm) :
    fullname = forms.CharField(label=_('Fullname'), max_length=100)

    email = forms.EmailField(label=_('Email Address'))

    class Meta :
        model = User
        fields = ('fullname', 'email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fullname'].required = False
        self.fields['fullname'].widget.attrs.update({'placeholder': _('Fullname'), })
        self.fields['email'].required = False
        self.fields['email'].widget.attrs.update({'placeholder': _('Email'), })

class ProfileDataForm (forms.ModelForm) :

    class Meta :
        model = Profile
        fields = ('bio', 'company', 'website', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['company'].required = False
        self.fields['website'].required = False

        self.fields['bio'].widget.attrs.update({'placeholder': _('Tell us a bit about yourself'), 'rows' : 5})
        self.fields['company'].widget.attrs.update({'placeholder': _('Company'), 'rows' : 3})
        self.fields['website'].widget.attrs.update({'placeholder': _('Company website'), })

class ProfileAvatarForm (forms.ModelForm) :
    avatar = forms.ImageField(label=_('Profile Picture'), error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)

    class Meta :
        model = Profile
        fields = ('avatar',)

    def clean_avatar (self) :
        picture = self.cleaned_data['avatar']
        if not picture:
            raise forms.ValidationError(_("No image!"))

        w, h = get_image_dimensions(picture)
        if w > settings.PROFILE_WIDTH or h > settings.PROFILE_HEIGHT:
            raise forms.ValidationError(_('Width and height of the image is more than {}').format(settings.PROFILE_WIDTH))

        if picture.size > settings.PROFILE_MAX_SIZE :
            raise forms.ValidationError(_('Profile image can not be over {} mb').format(settings.PROFILE_MAX_SIZE/1024/1024))

        return picture

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False

class ChangePassword(SetNewPasswordForm) :
    old_password = forms.CharField(label=_('Old Password'), widget=forms.PasswordInput)

    field_order = ('old_password', 'password', 'password1', )

    def clean_old_password(self) :
        password = self.cleaned_data['old_password']
        if not self.related_user.check_password(password):
            raise forms.ValidationError(_('Invalid password'))

    def __init__(self, user, *args,**kwargs):
        self.related_user = user
        super().__init__(*args,**kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': _('old password'), })
        self.fields['password'].widget.attrs.update({'placeholder': _('password'), })
        self.fields['password1'].widget.attrs.update({'placeholder': _('new password'), })