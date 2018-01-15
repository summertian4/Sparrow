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
from Sparrow.action import ApiAction
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', action.index, name='index'),
    # path('error', action.error),
    # # path('manager/api/list', ApiAction.list),
    # path('manage/api/create', ApiAction.create),
    # path('manage/api/detail/<api_id>', ApiAction.detail),
    # path('manage/api/update/<api_id>', ApiAction.update),
    # path('manage/api/delete/<api_id>', ApiAction.delete),
    # path('api/<path>', action.dispatch),
    # url(r'^api/', include('Sparrow.urls', namespace='api')),
    # url(r'^$', TemplateView.as_view(template_name="index.html")),
]