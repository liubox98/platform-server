from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from modules.users.models import UserInfo


# Create your models here.
class TaskInfo(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)
    creator = models.CharField(max_length=225)
    status = models.CharField(max_length=255)
    grade = models.CharField(max_length=255, default='高, 中, 低')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'task_info'
        unique_together = ('id', 'name',)


class TaskEventLog(models.Model):
    event_type = models.CharField(max_length=255)
    task = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    operator = models.CharField(max_length=255)

    class Meta:
        db_table = 'task_event_log'


@receiver(post_save, sender=TaskInfo)
def create_task_event_log_on_save(sender, instance, created, **kwargs):
    if created:
        event_type = '新增'
    else:
        event_type = '修改'
    TaskEventLog.objects.create(event_type=event_type, task=instance.name, timestamp=timezone.now(),
                                operator=instance.creator)


@receiver(pre_delete, sender=TaskInfo)
def create_task_event_log_on_delete(sender, instance, **kwargs):
    TaskEventLog.objects.create(event_type='删除', task=instance.name, timestamp=timezone.now(),
                                operator=instance.creator)


post_save.connect(create_task_event_log_on_save, sender=TaskInfo)
pre_delete.connect(create_task_event_log_on_delete, sender=TaskInfo)
