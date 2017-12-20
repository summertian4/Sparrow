from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from DAO.models import Api
from DAO.dao import ApiDao
import json
from django.core import serializers
from django.http import HttpResponseRedirect
from SparrowAdmin import *
from SparrowAdmin.forms import *
import SparrowAdmin._const

def index(request):
    context          = {}
    context['website_name'] = 'Sparrow'
    apis = list(ApiDao.getAllApis().values('api_id', 'path', 'method', 'name', 'note', 'status'))
    context['apis'] = apis
    return render(request, 'index.html', context)

def error(request):
    context = {}
    errorMessage = "出错了"
    if SparrowAdmin._const.kError in request.POST:
        errorMessage = request.POST[SparrowAdmin._const.kError]
    context["errorMessage"] = errorMessage

    return render(request, 'error.html', context)

def dispatch(request, api_name):
    response_data = {}
    response_data['api_name'] = api_name
    if request.method == 'POST':
        response_data['request'] = request.POST
        response_data['method'] = 'POST'
    else:
        response_data['request'] = request.GET
        response_data['method'] = 'GET'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

class ApiAction:
    def list(request):
        response_data = {}
        apis_list = list(ApiDao.getAllApis().values('api_id', 'path', 'method', 'name', 'note', 'status'))
        response_data['apis'] = apis_list
        response_data['method'] = 'GET'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def create(request):
        if request.method == 'POST':
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
                if ApiDao.create(model):
                    # todo: 返回到详情页面
                    return HttpResponseRedirect('/')
                else:
                    # todo: 返回到失败页面
                    return HttpResponseRedirect('/')
            else:
                # todo: 返回到失败页面
                return HttpResponseRedirect('/')
        if request.method == 'GET':
            context = {}
            return render(request, 'create.html', context)

    def update(request, api_id):
        context = {}
        return render(request, 'create.html', context)

    def delete(request, api_id):
        context = {}
        return render(request, 'index.html', context)