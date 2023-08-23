from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from modules.automation.auto.models import AutoInfo
from modules.automation.autorun.models import RunInfo
from modules.automation.autorun.views import RunInfoSerializer
from modules.automation.temp.models import TempInfo
from modules.users.models import UserInfo
from utils.response import APIResponse
from rest_framework import serializers


class TempInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempInfo
        fields = '__all__'  # Include all fields, you can specify the fields you want to include if needed


def check_uniqueness(name):
    name_list = set(TempInfo.objects.values_list('modules', flat=True))
    return name in name_list


@api_view(['GET'])
def temp_list(request):
    modules = request.query_params.get('name')
    auto_info = TempInfo.objects.all()
    if modules:
        auto_info = auto_info.filter(modules=modules)
    auto_info = auto_info.order_by('id')
    serializer = TempInfoSerializer(auto_info, many=True)
    result = serializer.data
    return APIResponse(code=200, msg="success",
                       data={'result': result, 'total': auto_info.count()})


@api_view(['post'])
def delete_temp(request):
    request_data = request.data
    task_obj = TempInfo.objects.filter(id=request_data.get('id')).delete()

    if task_obj:
        return APIResponse(code=200, msg="success")
    else:
        return APIResponse(code=500, msg="fail")


@api_view(['POST'])
def update_temp(request):
    request_data = request.data
    task_obj = get_object_or_404(TempInfo, id=request_data.get('id'))
    temp_serializer = TempInfoSerializer(instance=task_obj, data=request_data)
    if check_uniqueness(request_data['modules']) and task_obj.modules != request_data['modules']:
        return APIResponse(code=200, msg='任务重复')
    if temp_serializer.is_valid():
        temp_serializer.save()
        return APIResponse(code=200, msg='success')
    else:
        return APIResponse(code=500, msg='fail')


@api_view(['POST'])
def create_temp(request):
    request_data = request.data
    if check_uniqueness(request_data['modules']):
        return APIResponse(code=200, msg="模块存在")

    serializer_class = TempInfoSerializer(data=request_data)
    serializer_class.is_valid(raise_exception=True)
    task_obj = serializer_class.save()
    return APIResponse(code=200, msg="success", data={'id': task_obj.id})


@api_view(['POST'])
def assign_list(request):
    task_id = request.data.get('id')
    obj = RunInfo.objects.filter(task_id=task_id)

    temp_modules = TempInfo.objects.filter(status='正常').values_list('modules', flat=True)

    q_objects = Q()
    for module in temp_modules:
        q_objects |= Q(modules=module)

    obj_with_temp_modules = obj.filter(q_objects)
    obj_modules = obj_with_temp_modules.values_list('modules', flat=True)

    temp_obj_to_include = TempInfo.objects.filter(status='正常').exclude(modules__in=obj_modules)
    run_info_serializer = RunInfoSerializer(obj_with_temp_modules, many=True)
    temp_info_serializer = TempInfoSerializer(temp_obj_to_include, many=True)

    users = UserInfo.objects.filter(is_tester=True).values_list('username', flat=True).distinct()

    return APIResponse(code=200, msg="success",
                       data={'result': run_info_serializer.data + temp_info_serializer.data, 'users': users})


@api_view(['POST'])
def assign(request):
    modules = request.data.get('modules')
    executor = request.data.get('executor')
    maintain = request.data.get('maintain')
    number = request.data.get('number')
    task_id_list = request.data.get('id').split(',')

    with transaction.atomic():
        for task_id_str in task_id_list:
            task_id = int(task_id_str)
            try:
                auto_info = AutoInfo.objects.select_for_update().get(id=task_id)
            except AutoInfo.DoesNotExist:
                continue

            name = auto_info.name
            run_info_to_delete = RunInfo.objects.filter(task_id=auto_info, modules=modules)
            if executor:
                if not run_info_to_delete.exists():
                    RunInfo.objects.create(task_id=auto_info, name=name, modules=modules, executor=executor,
                                           maintain=maintain, number=number)
                    auto_info.number += number
                    auto_info.save()
                else:
                    run_info_to_delete.delete()
                    auto_info.number -= number
                    auto_info.save()
                    RunInfo.objects.create(task_id=auto_info, name=name, modules=modules, executor=executor,
                                           maintain=maintain, number=number)
                    auto_info.number += number
                    auto_info.save()
            else:
                if run_info_to_delete.exists():
                    run_info_to_delete.delete()
                    auto_info.number -= number
                    auto_info.save()

    return APIResponse(code=200, msg="success")


@api_view(['POST'])
def assign_del(request):
    return None


@api_view(['POST'])
def details(request):
    task_id = request.data.get('id')
    temp_details = RunInfo.objects.filter(task_id__id=task_id).all()
    serializer = RunInfoSerializer(temp_details, many=True)
    auto_info = AutoInfo.objects.filter(id=task_id).values('start_time', 'end_time').first()
    return APIResponse(code=200, msg="success",
                       data={'result': serializer.data, 'start_time': auto_info['start_time'],
                             'end_time': auto_info['end_time']})
