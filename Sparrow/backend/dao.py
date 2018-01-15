from django.http import HttpResponse
from django.shortcuts import render
from backend.models import Api

class ApiDao:
    def create(model):
        api = Api.objects.create(path=model.path,
                                 method=model.method,
                                 name=model.name,
                                 note=model.note,
                                 status=model.status,
                                 responseJson=model.responseJson)
        return api

    def get_all_apis():
        apis = Api.objects.all()
        return apis

    def get_all_api_list():
        apis = list(ApiDao.get_all_apis().values('api_id',
                                               'path',
                                               'method',
                                               'name',
                                               'note',
                                               'status',
                                               'responseJson'))
        return apis

    def get_api_with_id(api_id):
        api = Api.objects.get(api_id=api_id)
        return api

    def get_api(path, method):
        api = Api.objects.get(path=path, method=method)
        return api

    def delete(api_id):
        deleted_count, _ = Api.objects.filter(api_id=api_id).delete()
        print("delete count: " + str(deleted_count))
        if deleted_count > 0:
            return True
        else:
            return False

    def delete_all(self):
        result = Api.objects.all().delete()

    def update(model):
        result = Api.objects.filter(api_id=model.api_id).update(path=model.path,
                                                                method=model.method,
                                                                name=model.name,
                                                                note=model.note,
                                                                status=model.status,
                                                                responseJson=model.responseJson)
        if result > 0:
            return True
        else:
            return False
