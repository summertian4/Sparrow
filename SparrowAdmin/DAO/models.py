from django.db import models
import uuid

# Create your models here.
class Api(models.Model):
    api_id = models.CharField(max_length=40, default=uuid.uuid1())
    path = models.CharField(max_length=128)
    method = models.CharField(max_length=8)
    name = models.CharField(max_length=128, null=True)
    note = models.CharField(max_length=512, null=True)
    status = models.IntegerField(default=0)
