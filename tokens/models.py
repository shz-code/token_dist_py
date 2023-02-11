from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime  
from django.utils.timezone import now  
import random

# Create your models here.
class Tag(models.Model):
    name = models.CharField(_("Name"),max_length=50,null=True,blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(_("Event"),max_length=50,null=True,blank=True)
    created_date = models.DateTimeField(default=now)
    event_date = models.DateTimeField(_("Event Date"),null=True,blank=True)
    token_dist_start = models.DateTimeField(_("Token Distribution Start"),null=True,blank=True)
    token_dist_end = models.DateTimeField(_("Token Distribution End"),null=True,blank=True)
    token_usage = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag,blank=True)
    distribution_place = models.CharField(_("Distribution"),max_length=100,null=True,blank=True)
    desc = models.TextField(_("Description"),null=True,blank=True)

    def __str__(self):
        return self.name
    
    def get_tags(self):
        tags = self.tags.all()
        return tags  

class Token(models.Model):
    event = models.ForeignKey(Event,verbose_name=_("Event"),on_delete=models.CASCADE,null=True,blank=True)
    token_serial = models.AutoField(_("Serial"),primary_key=True)

    class Meta:
        verbose_name_plural = "Tokens"
    
    def __str__(self):
        return f'{self.token_serial}'
