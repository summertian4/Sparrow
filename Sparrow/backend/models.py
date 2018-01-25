from django.db import models
from enum import Enum, unique
from django.forms.models import model_to_dict

class Dictable(object):
    def as_dict(self):
        dict = {}
        # exclude ManyToOneRel, which backwards to ForeignKey
        field_names = []
        for field in self._meta.get_fields():
            if 'ManyToOneRel' not in str(field) and 'ManyToManyRel' not in str(field):
                field_names.append(field.name)
        for name in field_names:
            field_instance = getattr(self, name)
            if field_instance.__class__.__name__ == 'ManyRelatedManager':
                model_dics = []
                for model in field_instance.all():
                    model_dics.append(model_to_dict(model))
                dict[name] = model_dics
                continue
            dict[name] = field_instance
        return dict

class Api(models.Model, Dictable):
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


class Project(models.Model, Dictable):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    note = models.CharField(max_length=512, null=True, default="")
    status = models.IntegerField(default=1)
    apis = models.ManyToManyField(Api)

    @unique
    class Status(Enum):
        Disabled = 0
        Abled = 1
