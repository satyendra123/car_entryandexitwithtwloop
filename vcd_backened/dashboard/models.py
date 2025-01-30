from django.db import models
from django.utils import timezone

class CarLog(models.Model):
    id = models.AutoField(primary_key=True)
    gate = models.CharField(max_length=64, null=False, blank=False)
    action = models.CharField(max_length=64, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Boomsig(models.Model):
    id = models.AutoField(primary_key=True)
    entryboom = models.CharField(max_length=1, default='N')
    entrysynctime = models.DateTimeField(default=timezone.now)
    exitboom = models.CharField(max_length=1, default='N')
    exitsynctime = models.DateTimeField(default=timezone.now)
    barrier_open_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'boomsig'
