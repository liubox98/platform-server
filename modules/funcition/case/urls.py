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

from modules.funcition.case.views import CaseList, CaseUpdate, UploadFile, AssignCase, CaseOperation, DeleteCase, \
    UpdateCaseOperation, TaskDetails, QuestionList, UpdateProblemCase, deleteQuestion, AssignDelete, AssignCaseOperation

urlpatterns = [
    path('list', CaseList.as_view()),
    path('update', CaseUpdate.as_view()),
    path('upload', UploadFile.as_view()),
    path('assign', AssignCase.as_view()),
    path('operation', CaseOperation.as_view()),
    path('assignCase', AssignCaseOperation.as_view()),
    path('updateCase', UpdateCaseOperation.as_view()),
    path('deleteCase', DeleteCase.as_view()),
    path('taskDetails', TaskDetails.as_view()),
    path('updateProblemCase', UpdateProblemCase.as_view()),
    path('problemCase', QuestionList.as_view()),
    path('problemCase/<int:id>', deleteQuestion.as_view()),
    path('assignDelete', AssignDelete.as_view()),
]
