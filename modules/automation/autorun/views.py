from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from modules.automation.auto.models import AutoInfo
from modules.automation.autorun.models import RunInfo
from modules.automation.autorun.run_pagination import RunPagination
from utils.response import APIResponse
from rest_framework import serializers


class RunInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunInfo
        fields = '__all__'  # Include all fields, you can specify the fields you want to include if needed


@api_view(['POST'])
def perform_task(request):
    name = request.query_params.get('name')
    module = request.query_params.get('module')
    creator = request.query_params.get('creator')
    username = request.data.get('username')
    run_info = RunInfo.objects.filter(executor=username)
    if name:
        run_info = run_info.filter(task_id__name=name)
    if module:
        run_info = run_info.filter(modules=module)
    if creator:
        run_info = run_info.filter(task_id__creator=creator)

    run_info = run_info.order_by('id')
    creator_list = AutoInfo.objects.values_list('creator', flat=True)
    result = RunPagination().paginate_queryset(run_info.values(), request)
    return APIResponse(code=200, msg="success",
                       data={'result': result, 'creator_list': creator_list, 'total': len(result)})


@api_view(['POST'])
def update_task_report(request):
    run_obj = get_object_or_404(RunInfo, id=request.data.get('id'))
    run_obj.report = request.data.get('report')
    run_obj.save()
    return APIResponse(code=200, msg='success')


@api_view(['POST'])
def update_task_status(request):
    task_obj = get_object_or_404(RunInfo, id=request.data.get('id'))
    task_obj.status = request.data.get('status')
    task_obj.save()
    return APIResponse(code=200, msg='success')


@api_view(['GET'])
def operation(request):
    task = request.query_params.get('task')
    module = request.query_params.get('modules')
    status = request.query_params.get('status')
    maintain = request.query_params.get('maintain')
    executor = request.query_params.get('executor')

    filters = {}

    if task:
        filters['task_id__name'] = task
    if module:
        filters['modules'] = module
    if status:
        filters['status'] = status
    if maintain:
        filters['maintain'] = maintain
    if executor:
        filters['executor'] = executor

    run_info = RunInfo.objects.filter(**filters).order_by('id')
    result = run_info.values()

    name_list = run_info.values_list('name', flat=True).distinct()
    module_list = run_info.values_list('modules', flat=True).distinct()
    status_list = run_info.values_list('status', flat=True).distinct()
    maintain_list = run_info.values_list('maintain', flat=True).distinct()
    executor_list = run_info.values_list('executor', flat=True).distinct()

    return APIResponse(code=200, msg='success', data={
        'result': result,
        'name_list': set(name_list),
        'module_list': set(module_list),
        'status_list': set(status_list),
        'maintain_list': set(maintain_list),
        'executor_list': set(executor_list),
    })
