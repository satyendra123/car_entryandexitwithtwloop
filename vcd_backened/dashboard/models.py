from django.db import models
from django.utils import timezone

class CarLog(models.Model):
    id = models.AutoField(primary_key=True)
    gate = models.CharField(max_length=64, null=False, blank=False)
    action = models.CharField(max_length=64, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)