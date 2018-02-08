from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from backend.dao.api_dao import ApiDao
from backend.dao.project_dao import ProjectDao
import json
from django.http import HttpResponseRedirect
from Sparrow.forms import *
import Sparrow._const
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from Sparrow.action.common_action import CommonData
from backend.models import Api
from Sparrow.action.common_action import *
from django.forms.models import model_to_dict

FormParseError = 1001
DaoOperationError = 1002
RequetMethodError = 1003
MissingParametersError = 1004
Success = 200


class ApiAction:
    def list(request, project_id):
        response_data = {}
        apis = ProjectDao.get_project_with_id(project_id).apis.order_by('-createTime')
        apis_dict = []
        for api in apis:
            apis_dict.append(api.as_dict())
        response_data['apis'] = apis_dict
        return HttpResponse(json.dumps(response_data, default=datetime2string), content_type="application/json")

    @csrf_exempt
    def create(request, project_id):
        if request.method == CommonData.Method.POST.value:
            form = ApiCreateForm(data=request.POST)
            # check whether it's valid:
            if form.is_valid():
                model = Api()
                model.path = form.clean().get('path')
                model.method = form.clean().get('method')
                model.name = form.clean().get('name')
                model.note = form.clean().get('note')
                model.status = form.clean().get('status')
                model.responseJson = form.clean().get('responseJson')
                api = ApiDao.create(model)
                project = ProjectDao.get_project_with_id(project_id)
                project.apis.add(api)
                project.save()
                if api is None:
                    data = CommonData.response_data(DaoOperationError, "API create faild")
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = CommonData.response_data(Success, "sucsses")
                    data['api'] = model_to_dict(api)
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(FormParseError, "form parse faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "GET is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def repeat_name_verification(request, project_id):
        if request.method == 'GET':
            if ('path' not in request.GET.keys()) or \
                ('method' not in request.GET.keys()):
                data = CommonData.response_data(MissingParametersError, "缺少参数")
                return HttpResponse(json.dumps(data), content_type="application/json")
            path = request.GET['path']
            api_id = request.GET['api_id']
            method = request.GET['method']
            if path is None:
                return
            api = ApiDao.get_apis_with_project_id_and_path(project_id, path).first()
            data = CommonData.response_data(Success, "Success")
            if api is None:
                data['repeatability'] = False
            else:
                data['api'] = api.as_dict()

                if 'api_id' in request.GET.keys():
                    if (str(api.api_id) == str(api_id)) and (str(api.method) == str(method)):
                        data['repeatability'] = False
                    else:
                        data['repeatability'] = True
                else:
                    data['repeatability'] = True
            return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "POST is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def detail(request, project_id, api_id):
        api = ApiDao.get_api_with_id(api_id=api_id)
        data = CommonData.response_data(Success, "Success")
        data['api'] = api.as_dict()
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    @csrf_exempt
    def update(request, project_id, api_id):
        if request.method == CommonData.Method.POST.value:
            form = ApiUpdateForm(data=request.POST)
            if form.is_valid():
                model = ApiDao.get_api_with_id(api_id)
                model.path = form.clean().get('path')
                model.method = form.clean().get('method')
                model.name = form.clean().get('name')
                model.note = form.clean().get('note')
                model.status = form.clean().get('status')
                model.responseJson = form.clean().get('responseJson')
                result = ApiDao.update(model)

                if result is False:
                    data = CommonData.response_data(DaoOperationError, "API update faild")
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = CommonData.response_data(Success, "Sucsses")
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(FormParseError, "Form parse faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "GET is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def delete(request, project_id, api_id):
        if request.method == 'GET':
            succesed = ApiDao.delete(api_id)
            if succesed:
                data = CommonData.response_data(Success, "Success")
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(DaoOperationError, "Delete Failed")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "GET is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")
