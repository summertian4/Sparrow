from django.http import HttpResponse
from django.shortcuts import render
from DAO.models import Api
import json

class ApiDao:
    def create(model):

        api = Api.objects.create(path=model.path, method=model.method, name=model.name, note=model.note, status=model.status)
        print(api.path)
        print(api.status)

        if api is None:
            return False
        else:
            return True

    def getAllApis():
        apis = Api.objects.all()
        return apis

    def getApis(name):
        apis = Api.objects.get(name=name)
        return apis
