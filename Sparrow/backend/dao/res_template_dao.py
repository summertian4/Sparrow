from backend.models import ResTemplate
import datetime


class ResTemplateDao:
    def create(model):
        resTemplate = ResTemplate.objects.create(name=model.name,
                                                           note=model.note,
                                                           mimeType=model.mimeType,
                                                           responseJson=model.responseJson)
        return resTemplate

    def get_all_res_templates():
        resTemplates = ResTemplate.objects.all()
        return resTemplates

    def get_all_res_template_list():
        resTemplates = list(ResTemplateDao.get_all_res_templates().values('res_template_id',
                                                                           'name',
                                                                           'note',
                                                                           'mimeType',
                                                                           'responseJson'))
        return resTemplates

    def get_res_template_with_id(id):
        resTemplates = ResTemplate.objects.get(res_template_id=id)
        return resTemplates

    def get_res_templates_with_project_id(project_id):
        resTemplates = ResTemplate.objects.filter(project__project_id=project_id)
        return resTemplates

    def get_res_templates_with_project_id_and_name(project_id, name):
        resTemplates = ResTemplate.objects.filter(project__project_id=project_id, name=name)
        return resTemplates

    def get_res_template_with_name(name):
        try:
            resTemplates = ResTemplate.objects.filter(name=name)
            return resTemplates.first()
        except:
            return None

    def delete(res_template_id):
        deleted_count, _ = ResTemplate.objects.filter(res_template_id=res_template_id).delete()
        if deleted_count > 0:
            return True
        else:
            return False

    def update(model):
        result = ResTemplate.objects.filter(res_template_id=model.res_template_id).update(
            name=model.name,
            note=model.note,
            mimeType=model.mimeType,
            responseJson=model.responseJson,
            updateTime=datetime.datetime.now())
        if result > 0:
            return True
        else:
            return False
