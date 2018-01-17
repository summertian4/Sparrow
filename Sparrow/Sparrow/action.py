from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from DAO.models import Api
from DAO.dao import ApiDao
import json
from django.http import HttpResponseRedirect
from Sparrow.forms import *
import Sparrow._const
from django.http import QueryDict
import ast
from django.views.decorators.csrf import csrf_exempt


def index(request):
    context = {}
    apis = ApiDao.get_all_api_list()
    context['apis'] = apis
    return render(request, 'index.html', context)

def error(request):
    context = {}
    errorMessage = "出错了"
    print(request.method)
    if Sparrow._const.kError in request.POST:
        errorMessage = request.POST[Sparrow._const.kError]
    if Sparrow._const.kError in request.GET:
        errorMessage = request.GET[Sparrow._const.kError]
    context["errorMessage"] = errorMessage

    return render(request, 'error.html', context)

@csrf_exempt
def dispatch(request, path):
    response_data = {}


    try:
        api = ApiDao.get_api(path, request.method)
    except:
        request.POST = QueryDict(Sparrow._const.kError + "=" + "API:" + path + " 不存在")
        return error(request)


    json_dic = ast.literal_eval(api.responseJson)
    return HttpResponse(json.dumps(json_dic), content_type="application/json")


class ApiAction:
    def list(request):
        response_data = {}
        apis_list = ApiDao.get_all_api_list()
        response_data['apis'] = apis_list
        response_data['method'] = Api.Method.GET.value
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def create(request):
        if request.method == Api.Method.POST.value:
            form = ApiCreateForm(data=request.POST)
            print(form)
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
                    # 返回到失败页面
                    request.method = Api.Method.POST.value
                    request.POST = QueryDict(Sparrow._const.kError + "=" + "创建 API 失败")
                    return error(request)
                else:
                    # 返回到详情页面
                    return HttpResponseRedirect("/manage/api/detail/" + str(api.api_id))
            else:
                # 返回到失败页面
                request.method = Api.Method.POST.value
                request.POST = QueryDict(Sparrow._const.kError + "=" + "创建 API 失败")
                return error(request)
        if request.method == Api.Method.GET.value:
            context = {}
            return render(request, 'api/create.html', context)

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
