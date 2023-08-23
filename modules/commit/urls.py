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
from drf_yasg2 import openapi

from modules.commit.views import commit_list, upload_commit_file, update_commit_status, notify_robot, \
    update_commit_is_ignore_status
from modules.users.views import UserInfoView, LoginView, UserLogoutView

# from modules.projects.views import ProjectViewSet

urlpatterns = [
    path('list', commit_list),
    path('upload', upload_commit_file),
    path('update', update_commit_status),
    path('notify', notify_robot),
    path('updateIgnore', update_commit_is_ignore_status)
]
