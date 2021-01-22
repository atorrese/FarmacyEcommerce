import datetime
from django.db import models
from django.utils.timezone import datetime

#Clase Base Para eliminacion
class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True