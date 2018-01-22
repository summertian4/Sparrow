from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from backend.dao.api_dao import ApiDao
import json
from django.http import HttpResponseRedirect
from Sparrow.forms import *
import Sparrow._const
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from enum import Enum, unique
from Sparrow.action.common_action import CommonData

FormParseError = 1001
DaoOperationError = 1002
RequetMethodError = 1003
Success = 200

class ApiAction:
    def list(request):
        response_data = {}
        apis_list = ApiDao.get_all_api_list()
        response_data['apis'] = apis_list
        response_data['method'] = Api.Method.GET.value
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    @csrf_exempt
    def create(request):
        if request.method == Api.Method.POST.value:
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
                if api is None:
                    data = CommonData.response_data(DaoOperationError, "API create faild")
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = CommonData.response_data(Success, "sucsses")
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(FormParseError, "form parse faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "GET is invalid")
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

    def delete(request, api_id):
        succesed = ApiDao.delete(api_id)
        if succesed:
            return HttpResponseRedirect('/')
        else:
            # 返回到失败页面
            request.method = Api.Method.POST.value
            request.POST = QueryDict(Sparrow._const.kError + "=" + "删除 API 失败")
            return error(request)
