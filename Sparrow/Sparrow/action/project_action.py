from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from backend.dao.project_dao import ProjectDao
from django.views.decorators.csrf import csrf_exempt
from Sparrow.action.common_action import CommonData
from Sparrow.action.common_action import *
from Sparrow.forms import *
from backend.models import Project

FormParseError = 1001
DaoOperationError = 1002
RequetMethodError = 1003
RequetParamsError = 1003
MissingParametersError = 1004
Success = 200


class ProjectAction:
    def list(request):
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

        project_list = ProjectDao.get_all_project_list(offset, limit)
        data = CommonData.response_data(Success, "Success")

        count = ProjectDao.get_all_projects_count()
        data["projects_data"] = {"projects": project_list,
                                  "current_page": page,
                                  "total": count,
                                  "limit": limit}

        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def detail(request, project_id):
        project = ProjectDao.get_project_with_id(project_id)
        data = CommonData.response_data(Success, "Success")
        data["project"] = model_to_dict(project)
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    @csrf_exempt
    def create(request):
        if request.method != CommonData.Method.POST.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

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
                data['project'] = model_to_dict(project)
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(FormParseError, "form parse faild")
            return HttpResponse(json.dumps(data), content_type="application/json")

    @csrf_exempt
    def update(request, project_id):
        if request.method != CommonData.Method.POST.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        form = ProjectUpateForm(data=request.POST)
        if form.is_valid():
            model = ProjectDao.get_project_with_id(project_id)
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.status = form.clean().get('status')
            result = ProjectDao.update(model)

            if result is False:
                data = CommonData.response_data(DaoOperationError, "Project update faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(Success, "sucsses")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(FormParseError, "Form parse faild")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def repeat_name_verification(request):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        if ('name' not in request.GET.keys()):
            data = CommonData.response_data(MissingParametersError, "缺少参数")
            return HttpResponse(json.dumps(data), content_type="application/json")
        name = request.GET['name']
        project = ProjectDao.get_project_with_Name(name)
        data = CommonData.response_data(Success, "Success")
        if project is None:
            data['repeatability'] = False
        else:
            data['api'] = project.as_dict()
            if 'project_id' in request.GET.keys():
                project_id = request.GET['project_id']
                if str(project.project_id) == str(project_id):
                    data['repeatability'] = False
                else:
                    data['repeatability'] = True
            else:
                data['repeatability'] = True
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def delete(request):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        project_id = request.GET['project_id']
        if project_id is None:
            data = CommonData.response_data(RequetParamsError, "project_id is None")
            return HttpResponse(json.dumps(data), content_type="application/json")
        succesed = ProjectDao.delete(project_id)
        if succesed:
            data = CommonData.response_data(Success, "Success")
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(DaoOperationError, "Delete Failed")
            return HttpResponse(json.dumps(data), content_type="application/json")
