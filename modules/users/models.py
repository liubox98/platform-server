from django.db import models
from django.utils import timezone


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    token = models.FileField(max_length=255, null=True)
    expires_time = models.IntegerField(verbose_name='token过期时间', null=True)
    role_id = models.IntegerField()
    is_tester = models.BooleanField()
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)

    # 指定名字创建数据表不加APP前缀
    class Meta:
        db_table = 'user_info'


class Role(models.Model):
    name = models.CharField(max_length=20, verbose_name='角色名字')
    description = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'role'
#
# class Permissions(models.Model):
#     name = models.IntegerField(null=False)
#     permission_id = models.IntegerField(null=False)
#
#
# class RolePermissions(models.Model):
#     group_id = models.IntegerField(null=False)
#     permission_id = models.IntegerField(null=False)
