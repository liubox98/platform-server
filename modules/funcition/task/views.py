from django.db.models import Count
from rest_framework.views import APIView
from modules.funcition.case.models import Case
from modules.funcition.task.models import TaskInfo, TaskEventLog
from modules.funcition.task.taskSerializer import TaskSerializer, TaskEventLogSerializer
from modules.funcition.task.task_filter import FilterByTaskName, FilterByTaskCreator
from modules.funcition.task.task_pagination import TaskPagination
from utils.response import APIResponse


# Create your views here.
class TaskInfoView(APIView):
    @staticmethod
    def post(request, *args):
        tasks = TaskInfo.objects.order_by('-status', '-id')
        CASES = Case.objects.all()
        filter_task = FilterByTaskName().filter_queryset(request, tasks)
        filter_task = FilterByTaskCreator().filter_queryset(request, filter_task)
        tasks_pagination = TaskPagination().paginate_queryset(filter_task, request=request)
        creator = list(set(tasks.values_list('creator', flat=True)))
        task_modules = CASES.values('modules', 'task_id', 'task_id__name', 'performer').annotate(Count('modules'))
        task_items = []
        for task in tasks_pagination:
            cases = CASES.filter(task_id=task.id)
            count = cases.count()
            passed = cases.filter(status="执行通过").count()
            failed = cases.filter(status="执行失败").count()
            expire = cases.filter(status="需求过期").count()
            undone = cases.filter(status="暂未实现").count()
            change = cases.filter(status="需求变更").count()
            try:
                rate_result = round((passed + failed + expire + undone + change) / count * 100, 2)
            except ZeroDivisionError:
                rate_result = 0
            prop_rate = str(rate_result) + '%'
            task_item = TaskSerializer(task).data
            task_item['count'] = count
            task_item['prop_rete'] = prop_rate
            task_items.append(task_item)
        return APIResponse(code=200, msg="success",
                           data={'items': task_items, 'total': tasks.count(), 'task_modules': task_modules,
                                 "creators": creator})


class UpdateTaskInfo(APIView):
    @staticmethod
    def post(request, *args):
        request_data = request.data
        task_obj = TaskInfo.objects.filter(id=request_data.get('id')).first()
        task_serializer = TaskSerializer(data=request_data, instance=task_obj)
        if TaskInfo.objects.exclude(id=request_data['id']).filter(name=request_data['name']).exists():
            return APIResponse(code=200, msg='任务重复')
        if task_serializer.is_valid():
            task_serializer.save()
            return APIResponse(code=200, msg='success')
        else:
            return APIResponse(code=500, msg='fail')


class CreateTask(APIView):
    @staticmethod
    def post(request, *args):
        task_name = []
        for name in list(TaskInfo.objects.values('name')):
            task_name.append(name['name'])
        request_data = request.data
        print(request_data, 'request_data')
        if request_data['name'] in task_name:
            return APIResponse(code=200, msg="任务重复")
        task_ser = TaskSerializer(data=request_data)
        if task_ser.is_valid(raise_exception=True):
            task_obj = task_ser.save()
            return APIResponse(code=200, msg="success", data={'id': task_obj.id})
        else:
            return APIResponse(code=500, msg="fail")


class DeleteTask(APIView):

    @staticmethod
    def post(request, *args):
        request_data = request.data
        task_obj = TaskInfo.objects.get(id=request_data.get('id')).delete()
        if task_obj:
            return APIResponse(code=200, msg="success")
        else:
            return APIResponse(code=500, msg="fail")


class ResetCaseStatus(APIView):

    @staticmethod
    def post(request, *args):
        task_id = request.data['id']
        if Case.objects.filter(task_id=task_id).exists():
            Case.objects.filter(task_id=task_id).update(status='未执行')
            return APIResponse(code=200, msg='success', )
        return APIResponse(code=200, msg='用例未上传', )


class RetractCase(APIView):

    @staticmethod
    def post(request, *args):
        task_id = request.data['id']
        if Case.objects.filter(task_id=task_id).exists():
            Case.objects.filter(task_id=task_id).update(performer=None)
            return APIResponse(code=200, msg='success', )
        return APIResponse(code=200, msg='用例未上传', )


class EventLogListView(APIView):
    @staticmethod
    def get(request, *args):
        event_logs = TaskEventLog.objects.all()
        serializer = TaskEventLogSerializer(event_logs, many=True)
        data_list = [item for item in serializer.data]
        return APIResponse(code=200, data=data_list)


class Visual(APIView):
    @staticmethod
    def get(request, *args):
        tasks = TaskInfo.objects.annotate(case_count=Count('case'))
        data = {
            'title': list(tasks.values_list('name', flat=True)),
            'number': list(tasks.values_list('case_count', flat=True))
        }
        return APIResponse(code=200, data=data)
