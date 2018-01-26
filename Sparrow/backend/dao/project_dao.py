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

    def get_project_with_id(project_id):
        try:
            project = Project.objects.get(project_id=project_id)
            return project
        except:
            return None

    def get_project_with_Name(name):
        try:
            project = Project.objects.get(name=name)
            return project
        except:
            return None

    def create(model):
        project = Project.objects.create(name=model.name,
                                         note=model.note,
                                         status=model.status)
        return project

    def update(model):
        result = Project.objects.filter(project_id=model.project_id).update(name=model.name,
                                         note=model.note,
                                         status=model.status)
        if result > 0:
            return True
        else:
            return False
