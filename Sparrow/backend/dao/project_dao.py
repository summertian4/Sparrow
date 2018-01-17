from backend.models import Project
from backend.models import Api

class ProjectDao:
    def get_all_projects():
        projects = Project.objects.all()
        return projects

    def get_all_project_list():
        prjects = list(ProjectDao.get_all_projects().values('project_id',
                                               'name',
                                               'note',
                                               'status'))
        return prjects

    def get_project_with_id(project_id):
        project = Project.objects.get(project_id=project_id)
        return project