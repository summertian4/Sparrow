"""SparrowAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from Sparrow import action
from Sparrow.action.api_action import ApiAction
from Sparrow.action.project_action import ProjectAction
from Sparrow.action.res_template_action import ResTemplateAction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', action.common_action.index, name='index'),

    path('frontend/project/list', ProjectAction.list),
    path('frontend/project/detail/<project_id>', ProjectAction.detail),
    path('frontend/project/create', ProjectAction.create),
    path('frontend/project/update/<project_id>', ProjectAction.update),
    path('frontend/project/repeat_name_verification', ProjectAction.repeat_name_verification),
    path('frontend/project/delete', ProjectAction.delete),

    path('mock/<project_id>/<path:path>', action.common_action.mock),
    path('frontend/api/fetch', ApiAction.fetch),
    path('frontend/project/<project_id>/api/create', ApiAction.create),
    path('frontend/project/<project_id>/api/list', ApiAction.list),
    path('frontend/project/<project_id>/api/repeat_name_verification', ApiAction.repeat_name_verification),
    path('frontend/project/<project_id>/api/delete/<api_id>', ApiAction.delete),
    path('frontend/project/<project_id>/api/detail/<api_id>', ApiAction.detail),
    path('frontend/project/<project_id>/api/update/<api_id>', ApiAction.update),
    path('frontend/project/<project_id>/api/star/<api_id>', ApiAction.star),
    path('frontend/project/<project_id>/api/<api_id>/update_status', ApiAction.update_status),

    path('frontend/favorite/list', ApiAction.starList),

    path('frontend/res_template/list', ResTemplateAction.list),
    path('frontend/res_template/detail/<res_template_id>', ResTemplateAction.detail),
    path('frontend/res_template/create', ResTemplateAction.create),
    path('frontend/res_template/repeat_name_verification', ResTemplateAction.repeat_name_verification),
    path('frontend/res_template/delete/<res_template_id>', ResTemplateAction.delete),
    path('frontend/res_template/update/<res_template_id>', ResTemplateAction.update),
    # url(r'^api/', include('Sparrow.urls', namespace='api')),
    # url(r'^$', TemplateView.as_view(template_name="index.html")),
]
