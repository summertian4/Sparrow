from django.forms.models import model_to_dict
import json
from backend.dao.res_template_dao import ResTemplateDao
from Sparrow.action.common_action import *
from Sparrow.forms import *
from backend.models import ResTemplate

FormParseError = 1001
DaoOperationError = 1002
RequetMethodError = 1003
RequetParamsError = 1003
MissingParametersError = 1004
Success = 200

class ResTemplateAction:
    def list(request):
        resTemplates = ResTemplateDao.get_all_res_template_list()
        data = CommonData.response_data(Success, "Success")
        data["res_templates"] = resTemplates
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def detail(request, res_template_id):
        isOriginal = True
        if 'isOriginal' in request.GET.keys():
            isOriginal = False
        res_template = ResTemplateDao.get_res_template_with_id(res_template_id)

        if isOriginal == False:
            res_template.responseJson = json.loads(res_template.responseJson)
        dic = model_to_dict(res_template)
        if res_template.mimeType == ResTemplate.MIMEType.ApplicationJson:
            dic['mimeType'] = "application/json"
        elif res_template.mimeType == ResTemplate.MIMEType.TextPlain:
            dic['mimeType'] = "text/plain"
        elif res_template.mimeType == ResTemplate.MIMEType.ImageJpeg:
            dic['mimeType'] = "image/jpeg"

        dic['mimeType'] = "image/jpeg"
        print(dic['mimeType'])

        data = CommonData.response_data(Success, "Success")
        data["res_template"] = dic

        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    @csrf_exempt
    def create(request):
        if request.method == CommonData.Method.POST.value:
            form = ResTemplateCreateForm(data=request.POST)
            if form.is_valid():
                model = ResTemplate()
                model.name = form.clean().get('name')
                model.note = form.clean().get('note')
                model.type = form.clean().get('type')
                model.responseJson = form.clean().get('responseJson')
                resTemplate = ResTemplateDao.create(model)
                if resTemplate is None:
                    data = CommonData.response_data(DaoOperationError, "Response template create faild")
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = CommonData.response_data(Success, "Sucsses")
                    data['res_template'] = model_to_dict(resTemplate)
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(FormParseError, "Form parse faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "GET is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

    @csrf_exempt
    def update(request, project_id):
        if request.method == CommonData.Method.POST.value:
            form = ProjectUpateForm(data=request.POST)
            if form.is_valid():
                model = ResTemplateDao.get_project_with_id(project_id)
                model.name = form.clean().get('name')
                model.note = form.clean().get('note')
                model.status = form.clean().get('status')
                result = ResTemplateDao.update(model)

                if result is False:
                    data = CommonData.response_data(DaoOperationError, "Response template update faild")
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = CommonData.response_data(Success, "sucsses")
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(FormParseError, "Form parse faild")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "GET is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def repeat_name_verification(request):
        if request.method == 'GET':
            if ('name' not in request.GET.keys()):
                data = CommonData.response_data(MissingParametersError, "缺少参数")
                return HttpResponse(json.dumps(data), content_type="application/json")
            name = request.GET['name']
            resTemplate = ResTemplateDao.get_res_template_with_name(name)

            print(resTemplate)

            data = CommonData.response_data(Success, "Success")
            if resTemplate is None:
                data['repeatability'] = False
            else:
                data['resTemplate'] = resTemplate.as_dict()
                if 'project_id' in request.GET.keys():
                    project_id = request.GET['project_id']
                    if str(resTemplate.project_id) == str(project_id):
                        data['repeatability'] = False
                    else:
                        data['repeatability'] = True
                else:
                    data['repeatability'] = True
            return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "POST is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

    def delete(request):
        if request.method == 'GET':
            project_id = request.GET['project_id']
            if project_id is None:
                data = CommonData.response_data(RequetParamsError, "project_id is None")
                return HttpResponse(json.dumps(data), content_type="application/json")
            succesed = ResTemplateDao.delete(project_id)
            if succesed:
                data = CommonData.response_data(Success, "Success")
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = CommonData.response_data(DaoOperationError, "Delete Failed")
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(RequetMethodError, "GET is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")
