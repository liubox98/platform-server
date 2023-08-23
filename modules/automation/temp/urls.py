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
from django.urls import path
from modules.automation.temp.views import temp_list, delete_temp, update_temp, create_temp, assign_list, assign, \
    assign_del, details

# from modules.projects.views import ProjectViewSet
urlpatterns = [
    path('list', temp_list),
    path('delete', delete_temp),
    path('update', update_temp),
    path('create', create_temp),
    path('getAssign', assign_list),
    path('assign', assign),
    path('assignDel', assign_del),
    path('getDetails', details),
]
