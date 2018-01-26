from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from backend.dao.project_dao import ProjectDao
from django.views.decorators.csrf import csrf_exempt
from Sparrow.action.common_action import CommonData
from Sparrow.forms import *
from backend.models import Project

FormParseError = 1001
DaoOperationError = 1002
RequetMethodError = 1003
Success = 200


class ProjectAction:
    def list(request):
        response_data = {}
        project_list = ProjectDao.get_all_project_list()
        response_data["projects"] = project_list
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def detail(request, project_id):
        response_data = {}

        project = ProjectDao.get_project_with_id(project_id)
        response_data["project"] = project.as_dict()
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    @csrf_exempt
    def create(request):
        if request.method == CommonData.Method.POST.value:
            form = ProjectCreateForm(data=request.POST)
            if form.is_valid():
                model = Project()
                model.name = form.clean().get('name')
                model.note = form.clean().get('note')
                model.status = form.clean().get('status')
                project = ProjectDao.create(model)
                if project is None:
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

    @csrf_exempt
    def update(request, api_id):
        if request.method == CommonData.Method.POST.value:
            form = ProjectUpateForm(data=request.POST)
            if form.is_valid():
                model = ProjectDao.get_project_with_id(api_id)
                model.name = form.clean().get('name')
                model.note = form.clean().get('note')
                model.status = form.clean().get('status')
                result = ProjectDao.update(model)

                if result is False:
                    data = CommonData.response_data(DaoOperationError, "API update faild")
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

    def search(request):
        if request.method == 'GET':
            name = request.GET['name']
            project = ProjectDao.get_project_with_Name(name)
            data = CommonData.response_data(Success, "Success")
            if project is None:
                data['exist'] = False
            else:
                data['api'] = project.as_dict()
                data['exist'] = True
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "POST is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")
