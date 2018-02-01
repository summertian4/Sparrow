from backend.models import Project
import datetime


class ProjectDao:
    def get_all_projects():
        projects = Project.objects.all()
        return projects

    def get_all_project_list():
        prjects = list(ProjectDao.get_all_projects().values('project_id',
                                                            'name',
                                                            'note',
                                                            'status',
                                                            'createTime',
                                                            'updateTime'))
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
                                                                            status=model.status,
                                                                            updateTime=datetime.datetime.now())
        if result > 0:
            return True
        else:
            return False

    def delete(project_id):
        deleted_count, _ = Project.objects.filter(project_id=project_id).delete()
        print("delete count: " + str(deleted_count))
        if deleted_count > 0:
            return True
        else:
            return False
