from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from fcm_django.models import AbstractFCMDevice


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_('Фамилия'))
    patronymic = models.CharField(max_length=100, blank=True, verbose_name=_('Отчество'))


class Coordinate(AbstractFCMDevice):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    last_online_data = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_fcm_coordinate'
        verbose_name = _("FCM device")
        verbose_name_plural = _("FCM devices")

        indexes = [
            models.Index(fields=["registration_id", "user"]),
        ]
