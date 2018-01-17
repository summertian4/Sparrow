from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from backend.dao.project_dao import ProjectDao
from backend.models import Dictable
from django.core import serializers


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