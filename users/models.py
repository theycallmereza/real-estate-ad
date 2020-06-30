from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        _('شماره موبایل'),
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'09(\d{9})$')])
    phone_number_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
