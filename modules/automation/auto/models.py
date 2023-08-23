from django.db import models


# Create your models here.

class AutoInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name='任务名')
    description = models.CharField(null=True, blank=True, max_length=255, verbose_name='描述')
    creator = models.CharField(max_length=225, verbose_name='创建人')
    status = models.CharField(max_length=255, default='进行中', verbose_name='状态')
    number = models.IntegerField(default=0, verbose_name='用例数量')
    performer = models.CharField(null=True, blank=True, max_length=255, verbose_name='分配人')
    start_time = models.DateTimeField(null=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, verbose_name='结束时间')