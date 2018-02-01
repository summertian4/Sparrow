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

    def search(request, project_id):
        if request.method == 'GET':
            path = request.GET['path']
            if path is None:
                return
            api = ApiDao.get_apis_with_project_id_and_path(project_id, path).first()
            data = CommonData.response_data(Success, "Success")
            if api is None:
                data['repeatability'] = False
            else:
                data['api'] = api.as_dict()
                if 'api_id' in request.GET.keys():
                    api_id = request.GET['api_id']
                    if str(api.api_id) == str(api_id):
                        data['repeatability'] = False
                    else:
                        data['repeatability'] = True
                else:
                    data['repeatability'] = True
            return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "POST is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def detail(request, api_id):
        context = {}
        api = ApiDao.get_api_with_id(api_id=api_id)
        context['api'] = api
        return render(request, 'api/detail.html', context)

    def update(request, api_id):
        if request.method == Api.Method.POST.value:
            form = ApiUpdateForm(data=request.POST)
            print(form)
            # check whether it's valid:
            request.POST
            if form.is_valid():
                model = Api()
                model.api_id = api_id
                model.path = form.clean().get('path')
                model.method = form.clean().get('method')
                model.name = form.clean().get('name')
                model.note = form.clean().get('note')
                model.status = form.clean().get('status')
                model.responseJson = form.clean().get('responseJson')
                if ApiDao.update(model):
                    # 返回到详情页面
                    return HttpResponseRedirect("/manage/api/detail/" + api_id)
                else:
                    # 返回到失败页面
                    request.method = Api.Method.POST.value
                    request.POST = QueryDict(Sparrow._const.kError + "=" + "更新 API 失败")

                    return error(request)
            else:
                # 返回到失败页面
                request.method = Api.Method.POST.value
                request.POST = QueryDict(Sparrow._const.kError + "=" + "更新 API 失败,表单解析失败")
                return error(request)
            return HttpResponseRedirect('/')
        else:
            context = {}
            api = ApiDao.get_api_with_id(api_id)
            context['api'] = api
            return render(request, 'api/update.html', context)

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
