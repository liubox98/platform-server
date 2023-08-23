from django.db import models


# Create your models here.


class Case(models.Model):
    task_id = models.ForeignKey('task.TaskInfo', on_delete=models.CASCADE, db_constraint=False)
    modules = models.CharField(max_length=255)
    submodule = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    need = models.CharField(null=True, max_length=255)
    precondition = models.TextField()
    steps = models.TextField()
    results = models.TextField()
    type = models.CharField(null=True, max_length=255)
    status = models.CharField(blank=True, null=True, max_length=255)
    priority = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    performer = models.CharField(null=True, max_length=255)
    flag = models.BooleanField(null=True, max_length=255)
    remark = models.CharField(null=True, max_length=255)
    update_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'case'
