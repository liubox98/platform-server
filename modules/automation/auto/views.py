from django.shortcuts import get_object_or_404
from modules.automation.auto.auto_pagination import AutoPagination
from modules.automation.auto.models import AutoInfo
from utils.response import APIResponse
from rest_framework import serializers
from rest_framework.decorators import api_view


class AutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoInfo
        fields = '__all__'


def check_task_name_uniqueness(name):
    name_list = set(AutoInfo.objects.values_list('name', flat=True))
    return name in name_list


@api_view(['GET'])
def automated_task(request):
    name = request.query_params.get('name')
    creator = request.query_params.get('creator')
    auto_info = AutoInfo.objects.all()

    if name:
        auto_info = auto_info.filter(name=name)
    if creator:
        auto_info = auto_info.filter(creator=creator)
    auto_info = auto_info.order_by('id')
    creator_list = AutoInfo.objects.values_list('creator', flat=True).distinct()
    result = AutoPagination().paginate_queryset(auto_info.values(), request)
    return APIResponse(code=200, msg="success",
                       data={'result': result, 'creator_list': creator_list, 'total': len(result)})


@api_view(['POST'])
def add_task(request):
    request_data = request.data
    if check_task_name_uniqueness(request_data['name']):
        return APIResponse(code=200, msg="任务重复")

    serializer_class = AutoSerializer(data=request_data)
    serializer_class.is_valid(raise_exception=True)
    task_obj = serializer_class.save()
    return APIResponse(code=200, msg="success", data={'id': task_obj.id})


@api_view(['POST'])
def update_task(request):
    request_data = request.data
    task_obj = get_object_or_404(AutoInfo, id=request_data.get('id'))
    task_serializer = AutoSerializer(instance=task_obj, data=request_data)

    if check_task_name_uniqueness(request_data['name']) and task_obj.name != request_data['name']:
        return APIResponse(code=200, msg='任务重复')

    if task_serializer.is_valid():
        task_serializer.save()
        return APIResponse(code=200, msg='success')
    else:
        return APIResponse(code=500, msg='fail')


@api_view(['POST'])
def delete_task(request):
    request_data = request.data
    task_obj = AutoInfo.objects.filter(id=request_data.get('id')).delete()

    if task_obj:
        return APIResponse(code=200, msg="success")
    else:
        return APIResponse(code=500, msg="fail")
