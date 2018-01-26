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
import Sparrow.action.common_action
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', action.common_action.index, name='index'),
    # path('error', action.error),
    path('api/list', ApiAction.list),
    path('api/detail/<api_id>', ApiAction.detail),
    path('api/update/<api_id>', ApiAction.update),
    path('api/delete/<api_id>', ApiAction.delete),
    path('mock/api/<path>', action.common_action.dispatch),

    path('frontend/project/list', ProjectAction.list),
    path('frontend/project/detail/<project_id>', ProjectAction.detail),
    path('frontend/project/create', ProjectAction.create),
    path('frontend/project/update/<api_id>', ProjectAction.update),
    path('frontend/project/search', ProjectAction.search),
    path('frontend/api/create', ApiAction.create),
    path('frontend/api/search', ApiAction.search),
    # url(r'^api/', include('Sparrow.urls', namespace='api')),
    # url(r'^$', TemplateView.as_view(template_name="index.html")),
]
