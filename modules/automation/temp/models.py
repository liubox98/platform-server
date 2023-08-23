from django.db import models


# Create your models here.
class TempInfo(models.Model):
    modules = models.CharField(max_length=255, verbose_name='任务名')
    number = models.IntegerField(default=0, verbose_name='数量')
    status = models.CharField(max_length=20, default='正常', verbose_name='状态')
    maintain = models.CharField(max_length=255, default=None, verbose_name='维护人')
