from django.views.decorators.csrf import csrf_exempt
from backend.dao.api_dao import ApiDao
import Sparrow._const
from django.shortcuts import render
from django.http import HttpResponse
import json
from enum import Enum, unique
import datetime
from backend.models import Api

APINotExist = 1000
APINotOpenMock = 1005

def datetime2string(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

class CommonData(object):
    def response_data(code, message):
        dic = {'code': code, 'message': message}
        return dic

    @unique
    class Method(Enum):
        GET = "GET"
        POST = "POST"

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
def mock(request, project_id, path):
    method = str(request.method)
    api = ApiDao.get_api(path, method)

    if api is None:
        data = CommonData.response_data(APINotExist, "该 Method 的 API 不存在")
        return HttpResponse(json.dumps(data), content_type="application/json")
    if api.status != Api.Status.Mock.value:
        data = CommonData.response_data(APINotOpenMock, "该 API 没有开启 Mock")
        return HttpResponse(json.dumps(data), content_type="application/json")

    data = json.loads(api.responseJson)
    return HttpResponse(json.dumps(data), content_type="application/json")
