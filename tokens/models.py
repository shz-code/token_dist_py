from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime    
import random

# Create your models here.
class Token(models.Model):
    token_serial = models.AutoField(_("Serial"),primary_key=True)
    token_event = models.CharField(_("Event"),null=True,blank=True,max_length=100)

    class Meta:
        verbose_name_plural = "Tokens"
    
    def __str__(self):
        return f'{self.token_serial}'
