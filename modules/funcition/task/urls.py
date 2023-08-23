"""testerServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

from modules.funcition.task.views import TaskInfoView, UpdateTaskInfo, CreateTask, DeleteTask, ResetCaseStatus, \
    RetractCase, EventLogListView, Visual
from modules.users.views import UserInfoView, LoginView, UserLogoutView

# from modules.projects.views import ProjectViewSet

urlpatterns = [
    path('list', TaskInfoView.as_view()),
    path('update', UpdateTaskInfo.as_view()),
    path('create', CreateTask.as_view()),
    path('delete', DeleteTask.as_view()),
    path('resetCaseStatus', ResetCaseStatus.as_view()),
    path('retractCase', RetractCase.as_view()),
    path('activity', EventLogListView.as_view()),
    path('visual', Visual.as_view())
]
