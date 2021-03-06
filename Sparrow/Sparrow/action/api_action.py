from dal.dao.api_dao import ApiDao
from dal.dao.project_dao import ProjectDao
from Sparrow.forms import *
from dal.models import Api
from Sparrow.action.common_action import *
from django.forms.models import model_to_dict

FormParseError = 1001
DaoOperationError = 1002
RequetMethodError = 1003
MissingParametersError = 1004
Success = 200

class ApiAction:
    def list(request, project_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        limit = 10
        page = 1
        if 'limit' in request.GET.keys():
            limit = int(request.GET['limit'])
        if 'current_page' in request.GET.keys():
            page = int(request.GET['current_page'])

        offset = (page - 1) * limit

        apis = ApiDao.get_apis_with_project_id(project_id, offset, limit)
        apis_dict = []
        for api in apis:
            api_dic = api.as_dict()
            project_dic = ProjectDao.get_project_with_api_id(api.api_id)
            if project_dic is not None:
                api_dic['project'] = project_dic
            apis_dict.append(api_dic)

        count = ApiDao.get_apis_count_with_project_id(project_id)
        data = CommonData.response_data(Success, "Success")

        data["apis_data"] = {"apis": apis_dict,
                             "current_page": page,
                             "total": count,
                             "limit": limit}
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def fetch(request):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        if 'project_id[]' not in request.GET.keys():
            data = CommonData.response_data(MissingParametersError, "Missing Parameters")
            return HttpResponse(json.dumps(data), content_type="application/json")

        project_ids = request.GET.getlist('project_id[]')

        apis_dics = []
        for project_id in project_ids:
            aList = list(ApiDao.get_all_apis_with_project_id(project_id))
            for api in aList:
                api['project_id'] = int(project_id)
                apis_dics.append(api)

        data = CommonData.response_data(Success, "Success")
        data['apis'] = apis_dics
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    @csrf_exempt
    def create(request, project_id):
        if request.method != CommonData.Method.POST.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        form = ApiCreateForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            model = Api()
            model.path = form.clean().get('path')
            if model.path.startswith('/', ):
                model.path = model.path[1:]
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

    def repeat_name_verification(request, project_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        if ('path' not in request.GET.keys()) or \
                ('method' not in request.GET.keys()):
            data = CommonData.response_data(MissingParametersError, "缺少参数")
            return HttpResponse(json.dumps(data), content_type="application/json")
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
                if (str(api.api_id) == str(api_id)):
                    data['repeatability'] = False
                else:
                    data['repeatability'] = True
            else:
                data['repeatability'] = True
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def detail(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        isOriginal = True
        if 'isOriginal' in request.GET.keys():
            isOriginal = False
        api = ApiDao.get_api_with_id(api_id=api_id)
        data = CommonData.response_data(Success, "Success")
        if isOriginal == False:
            api.responseJson = json.loads(api.responseJson)
        data['api'] = api.as_dict()
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    @csrf_exempt
    def update(request, project_id, api_id):
        if request.method != CommonData.Method.POST.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        form = ApiUpdateForm(data=request.POST)
        if form.is_valid():
            model = ApiDao.get_api_with_id(api_id)
            model.path = form.clean().get('path')
            if model.path.startswith('/', ):
                model.path = model.path[1:]
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

    def delete(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        succesed = ApiDao.delete(api_id)
        if succesed:
            data = CommonData.response_data(Success, "Success")
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(DaoOperationError, "Delete Failed")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def star(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        api = ApiDao.get_api_with_id(api_id)
        if api is not None:
            api.star = not api.star
            print(api.star)
            result = ApiDao.update(api)
            if result is False:
                data = CommonData.response_data(DaoOperationError, "Update API Faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(Success, "Success")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(DaoOperationError, "API is not exist")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def starList(request):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        limit = 10
        page = 1
        if 'limit' in request.GET.keys():
            limit = int(request.GET['limit'])
        if 'current_page' in request.GET.keys():
            page = int(request.GET['current_page'])

        offset = (page - 1) * limit

        apis = ApiDao.get_all_stared_apis(offset, limit)
        apis_dict = []
        for api in apis:
            api_dic = api.as_dict()
            project_dic = ProjectDao.get_project_with_api_id(api.api_id)
            if project_dic is not None:
                api_dic['project'] = project_dic
            apis_dict.append(api_dic)
        count = ApiDao.get_stared_apis_count()
        data = CommonData.response_data(Success, "Success")
        data["apis_data"] = {"apis": apis_dict,
                             "current_page": page,
                             "total": count,
                             "limit": limit}
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def update_status(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        if ('status' not in request.GET.keys()):
            data = CommonData.response_data(MissingParametersError, "缺少参数")
            return HttpResponse(json.dumps(data), content_type="application/json")

        status = request.GET['status']
        api = ApiDao.get_api_with_id(api_id)
        if api is not None:
            api.status = status
            result = ApiDao.update(api)
            if result is False:
                data = CommonData.response_data(DaoOperationError, "Update API Faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(Success, "Success")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(DaoOperationError, "API is not exist")
            return HttpResponse(json.dumps(data), content_type="application/json")
