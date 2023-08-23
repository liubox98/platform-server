from django.db import models


# Create your models here.
class CommitInfo(models.Model):
    commit_hash = models.CharField(max_length=50, verbose_name='提交hash值')
    name = models.CharField(max_length=50, verbose_name='提交的姓名')
    detail = models.TextField(verbose_name='提交的姓名')
    version = models.CharField(max_length=50, verbose_name='提交版本')
    confire = models.BooleanField(default=False, verbose_name='是否确认合并')
    isIgnore = models.BooleanField(default=False, verbose_name='是否忽略')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
