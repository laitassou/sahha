from django.db import models
from django.contrib.auth.models import User as DjangoUser, AbstractUser
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.conf import settings

from sahha_service.utils import exceptions
from sahha_service.utils.helpers import logger
import uuid
from decimal import Decimal

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class SahhaUser(AbstractModel):
    STUDENT = 'Student'
    TEACHER = 'Teacher'
    MANAGER = 'Manager'
    SUPERVISOR = 'Supervisor'
    ROLE_CHOICES = (
        (STUDENT, STUDENT),    # worker
        (TEACHER, TEACHER),    # client
        (MANAGER, MANAGER),    # manager
        (SUPERVISOR, SUPERVISOR),
    )
    phone_number = models.CharField(max_length=128, null=True)
    degree = models.CharField(max_length=128, null=True, blank=True)
    django_user = models.OneToOneField(
        DjangoUser, on_delete=models.CASCADE, null=False, related_name='sahha_user')
    role = models.CharField(
        max_length=120, default=STUDENT, choices=ROLE_CHOICES)
    repr = "SahhaUser"

    def __str__(self):
        return '{}'.format(self.django_user)
