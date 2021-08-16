from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from persian_tools import phone_number

def validate_number(value):
    if not phone_number.validate(value) :
        raise ValidationError(
            _('%(value) is not a valid phone-number'),
            params={'value': value},
        )

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError(_('Users must have an username'))

        user = self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
                        username,
                        password
                    )

        user.is_active = True
        user.is_deleted = False
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=11, validators=[validate_number], unique=True, verbose_name=_('Username'))
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True, verbose_name=_('Email address'))
    fullname = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Fullname'))

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Signup date'))

    is_active = models.BooleanField(default=False, verbose_name=_('Account is active'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Account is deleted'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Account is admin'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Account is staff'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Account is superuser'))

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_fullName(self) :
        return f'{self.fullname}'

    def __str__(self) :
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
