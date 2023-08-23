import jwt
import json
import logging
from django.http import JsonResponse
from rest_framework.views import APIView
from utils.response import APIResponse
from modules.users.models import UserInfo, Role
from modules.users.serializers import UserSerializer, RoleSerializer


# Create your views here.
class UserInfoView(APIView):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    @staticmethod
    def get(request):
        token = request.query_params.get('token')
        user = UserInfo.objects.filter(token=token).first()
        if user:
            role_name = Role.objects.get(id=user.role_id).name
            return JsonResponse({'data': {'name': user.username, 'roles': [role_name], 'avatar': ''}})
        else:
            return JsonResponse({'data': ''})


class LoginView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        json_str = request.body
        json_dict = json.loads(json_str)
        print(json_dict)
        username = json_dict.get("username", None)
        password = json_dict.get("password", None)
        if username:
            # 判断用户名是否一致，
            try:
                user = UserInfo.objects.get(username=username)
            except Exception as e:
                logging.error(e)
                return JsonResponse({'code': 500, 'msg': '用户不存在/密码错误'})
            # 判断密码是否一致
            if user.password == password:
                b = {'username': username, 'password': password}
                token = jwt.encode(b, 'secret', algorithm='HS256')
                # 用户名和密码都满足，保存token到表中
                user.token = token
                user.save()
                return JsonResponse(
                    {'code': 20000, 'msg': '操作成功', 'data': {'token': token}, 'currentAuthority': username})
            else:
                return JsonResponse({'code': 500, 'msg': '密码错误'})
        else:
            return JsonResponse({'code': 500, 'msg': '用户名不存在'})


class UserLogoutView(APIView):
    @staticmethod
    def post(*args, **kwargs):
        return JsonResponse({'code': 20000, 'msg': '操作成功'})


class UserList(APIView):
    @staticmethod
    def get(request):
        users = UserInfo.objects.all()
        serialize = UserSerializer(users, many=True).data
        # print(UserInfo.objects.get(id=1).role_name)
        role = Role.objects.all()
        role_serialize = RoleSerializer(role, many=True).data
        return APIResponse(code=200, msg="success",
                           data={'user_list': serialize, 'role_list': role_serialize, 'total': len(users)})


class UserDelete(APIView):
    @staticmethod
    def delete(request, *args, **kwargs):
        user_id = kwargs['id']
        UserInfo.objects.filter(id=user_id).delete()
        # print(UserInfo.objects.get(id=1).role_name)

        return APIResponse(code=200, msg="success")


class UserAdd(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        if UserInfo.objects.filter(username=request_data['username']).exists():
            return APIResponse(code=500, msg="人员存在")
        user_obj = UserInfo()
        user_obj.role_id = request_data.get('role_id')
        user_obj.username = request_data.get('username')
        user_obj.is_tester = request_data.get('is_tester')
        user_obj.password = request_data.get('password')

        try:
            user_obj.save()
            print(user_obj)
            return APIResponse(code=200, msg="success", data={'id': user_obj.id})
        except Exception as e:
            print(e)
            return APIResponse(code=500, msg="fail")


class UserUpdate(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        request_data = request.data
        user_obj = UserInfo.objects.get(id=request_data.get('id'))
        print(request_data)
        user_obj.role_id = request_data.get('role_id')
        user_obj.username = request_data.get('username')
        user_obj.is_tester = request_data.get('is_tester')
        user_obj.password = request_data.get('password')
        try:
            user_obj.save()
            return APIResponse(code=200, msg="success")
        except Exception as e:
            print(e)
            return APIResponse(code=200, msg="fail")


class UserUpdatePassword(APIView):
    @staticmethod
    def post(request):
        username = request.data['username']
        if UserInfo.objects.get(username=username).password == request.data['password']:
            newpwd = request.data['newpwd']
            UserInfo.objects.filter(username=username).update(password=newpwd)
            return APIResponse(code=200, msg="success")
        else:
            return APIResponse(code=200, msg="fail")
