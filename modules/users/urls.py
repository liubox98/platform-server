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

from modules.users.views import UserInfoView, LoginView, UserLogoutView, UserList, UserDelete, UserAdd, UserUpdate, \
    UserUpdatePassword

# from modules.projects.views import ProjectViewSet


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login', LoginView.as_view()),
    path('info/', UserInfoView.as_view()),
    path('logout', UserLogoutView.as_view()),
    path('list', UserList.as_view()),
    path('delete/<int:id>', UserDelete.as_view()),
    path('add', UserAdd.as_view()),
    path('update', UserUpdate.as_view()),
    path('updatePassword', UserUpdatePassword.as_view())

]
