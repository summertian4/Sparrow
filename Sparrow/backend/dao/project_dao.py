from backend.models import Project

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