from django.db import models
from enum import Enum, unique

class Api(models.Model):
    api_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=128)
    method = models.CharField(max_length=8)
    name = models.CharField(max_length=128, null=True)
    note = models.CharField(max_length=512, null=True, default="")
    status = models.IntegerField(default=0)

    responseJson = models.TextField(default="", blank=True, null=True)

    @unique
    class Status(Enum):
        Disabled = 0
        Abled = 1

    @unique
    class Method(Enum):
        GET = "GET"
        POST = "POST"


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    note = models.CharField(max_length=512, null=True, default="")
    status = models.IntegerField(default=0)

    @unique
    class Status(Enum):
        Disabled = 0
        Abled = 1