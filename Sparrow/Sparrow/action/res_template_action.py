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
        resTemplates = ResTemplateDao.get_all_res_template_list(offset, limit)

        data = CommonData.response_data(Success, "Success")

        count = ResTemplateDao.get_all_res_template_count()
        data["templates_data"] = {"res_templates": resTemplates,
                                  "current_page": page,
                                  "total": count,
                                  "limit": limit}
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def detail(request, res_template_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        isOriginal = True
        if 'isOriginal' in request.GET.keys():
            isOriginal = False
        res_template = ResTemplateDao.get_res_template_with_id(res_template_id)

        if isOriginal == False:
            res_template.responseJson = json.loads(res_template.responseJson)
        dic = model_to_dict(res_template)

        data = CommonData.response_data(Success, "Success")
        data["res_template"] = dic

        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    @csrf_exempt
    def create(request):
        if request.method != CommonData.Method.POST.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

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

    @csrf_exempt
    def update(request, res_template_id):
        if request.method != CommonData.Method.POST.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        form = ResTemplateUpdateForm(data=request.POST)
        if form.is_valid():
            model = ResTemplateDao.get_res_template_with_id(res_template_id)
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.mimeType = form.clean().get('mimeType')
            model.responseJson = form.clean().get('responseJson')
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

    def repeat_name_verification(request):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        if ('name' not in request.GET.keys()):
            data = CommonData.response_data(MissingParametersError, "缺少参数")
            return HttpResponse(json.dumps(data), content_type="application/json")
        name = request.GET['name']
        resTemplate = ResTemplateDao.get_res_template_with_name(name)

        data = CommonData.response_data(Success, "Success")
        if resTemplate is None:
            data['repeatability'] = False
        else:
            data['resTemplate'] = resTemplate.as_dict()
            if 'res_template_id' in request.GET.keys():
                res_template_id = request.GET['res_template_id']
                if str(resTemplate.res_template_id) == str(res_template_id):
                    data['repeatability'] = False
                else:
                    data['repeatability'] = True
            else:
                data['repeatability'] = True
        return HttpResponse(json.dumps(data, default=datetime2string), content_type="application/json")

    def delete(request, res_template_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequetMethodError, "Method is invalid")
            return HttpResponse(json.dumps(data), content_type="application/json")

        succesed = ResTemplateDao.delete(res_template_id)
        if succesed:
            data = CommonData.response_data(Success, "Success")
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = CommonData.response_data(DaoOperationError, "Delete Failed")
            return HttpResponse(json.dumps(data), content_type="application/json")
