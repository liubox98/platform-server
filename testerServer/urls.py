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

from django.urls import path, include
from rest_framework import routers

# from modules.projects.views import ProjectViewSet

router = routers.DefaultRouter()
# router.register(r'projects', ProjectViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    # path('admin/', admin.site.urls),
    # path('api-users/', include('rest_framework.urls', namespace='rest_framework')),

    # 子路由
    path('api/user/', include('modules.users.urls')),
    path('api/task/', include('modules.funcition.task.urls')),
    path('api/case/', include('modules.funcition.case.urls')),
    path('api/commit/', include('modules.commit.urls')),
    path('api/auto/', include('modules.automation.auto.urls')),
    path('api/autorun/', include('modules.automation.autorun.urls')),
    path('api/temp/', include('modules.automation.temp.urls')),
]
