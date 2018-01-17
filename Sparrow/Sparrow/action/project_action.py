from django.http import HttpResponse
import json
from backend.dao.project_dao import ProjectDao

class ProjectAction:
    def list(request):
        response_data = {}
        project_list = ProjectDao.get_all_project_list()
        response_data["projects"] = project_list
        return HttpResponse(json.dumps(response_data), content_type="application/json")