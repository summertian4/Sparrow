from django.views.decorators.csrf import csrf_exempt
from backend.dao.api_dao import ApiDao
import Sparrow._const
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json

class CommonData(object):
    def response_data(code, message):
        dic = {'code': code, 'message': message}
        return dic

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
    response_data["name"] = "hello"
    # try:
    #     api = ApiDao.get_api(path, request.method)
    # except:
    #     request.POST = QueryDict(Sparrow._const.kError + "=" + "API:" + path + " 不存在")
    #     return error(request)
    #
    #
    # json_dic = ast.literal_eval(api.responseJson)
    # return HttpResponse(json.dumps(json_dic), content_type="application/json")
    return HttpResponse(json.dumps(response_data), content_type="application/json")

