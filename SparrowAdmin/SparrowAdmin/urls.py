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

from DAO.dao import ApiDao
from SparrowAdmin import action
from SparrowAdmin.action import ApiAction

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', action.index, name='index'),
    path('error', action.error),
    # path('manager/api/list', ApiAction.list),
    path('manage/api/create', ApiAction.create),
    path('manage/api/update/<api_id>', ApiAction.update),
    path('manage/api/delete/<api_id>', ApiAction.delete),
    path('api/<api_name>', action.dispatch),


]
