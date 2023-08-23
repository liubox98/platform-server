from django.db import models


# Create your models here.
class RunInfo(models.Model):
    task_id = models.ForeignKey('auto.AutoInfo', on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(max_length=255, verbose_name='任务名')
    modules = models.CharField(max_length=255, verbose_name='模块名')
    number = models.IntegerField(default=0, verbose_name='用例数量')
    executor = models.CharField(max_length=255, verbose_name='执行人')
    maintain = models.CharField(max_length=255, verbose_name='维护人')
    report = models.URLField(max_length=1000, blank=True, null=True, verbose_name='报告')
    status = models.CharField(blank=True, null=True, max_length=255, verbose_name='状态')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
