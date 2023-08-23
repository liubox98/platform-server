import datetime
import openpyxl
from django.db.models import Count
from rest_framework.views import APIView
from modules.funcition.case.case_pagination import CasePagination
from modules.funcition.case.case_filter import FilterByCaseId, FilterByCaseName, FilterByCaseModule, FilterByCaseSubmodule, \
    FilterByCaseStatus, FilterByCasePriority, FilterByCaseCreator, FilterByCasePerformer, FilterByCaseType, \
    FilterByCaseUnexecutedModule
from modules.funcition.case.models import Case
from modules.funcition.case.serializers import CaseSerializer
from modules.funcition.task.models import TaskInfo
from modules.users.models import UserInfo
from modules.users.serializers import UserSerializer
from utils.response import APIResponse


# Create your views here.
class CaseList(APIView):
    @staticmethod
    def post(request, *args):
        username = request.data['username']
        CASES = Case.objects.order_by('task_id_id')

        task_type = CASES.filter(performer=username, task_id__status='进行中').values('task_id__name').annotate(
            Count('task_id__name'))
        task_tags, query_list = [], []
        for info in range(len(task_type)):
            grade_list = list(TaskInfo.objects.filter(name=task_type[info]['task_id__name']).values('grade'))
            query_list += list(
                CASES.filter(task_id__name=task_type[info]['task_id__name'], performer=username,
                             task_id__status='进行中', priority__in=grade_list[0]['grade']))
            cases = CASES.filter(task_id__name=task_type[info]['task_id__name'], performer=username,
                                 priority__in=list(grade_list[0]['grade']))
            fenpei = cases.count()
            passed = cases.filter(status="执行通过").count()
            failed = cases.filter(status="执行失败").count()
            expire = cases.filter(status="需求过期").count()
            undone = cases.filter(status="暂未实现").count()
            change = cases.filter(status="需求变更").count()
            try:
                rate_result = round((passed + failed + expire + undone + change) / fenpei * 100, 2)
            except ZeroDivisionError:
                rate_result = 0
            prop_rete = rate_result if rate_result != 0 else '0'
            task_tags.append({'name': task_type[info]['task_id__name'], 'prop_rete': prop_rete})
        result = CASES.filter(pk__in=[x.pk for x in query_list])
        filter_case = FilterByCaseId().filter_queryset(request, result.order_by('id'))
        filter_case = FilterByCaseName().filter_queryset(request, filter_case)
        filter_case = FilterByCaseModule().filter_queryset(request, filter_case)
        filter_case = FilterByCaseUnexecutedModule().filter_queryset(request, filter_case)
        filter_case = FilterByCaseSubmodule().filter_queryset(request, filter_case)
        filter_case = FilterByCaseStatus().filter_queryset(request, filter_case)
        cases_pagination = CasePagination().paginate_queryset(filter_case, request=request)
        case_items = CaseSerializer(cases_pagination, many=True).data

        task_status = CASES.values('status').annotate(Count('status'))
        modules_type = CASES.filter(performer=username, task_id__status='进行中').values('modules').annotate(
            Count('modules'))
        unexecuted_module = CASES.filter(performer=username, task_id__status='进行中', status='未执行').values(
            'modules').annotate(Count('modules'))

        return APIResponse(code=200, msg='success',
                           data={'total': len(filter_case), 'items': case_items, 'modules_type': modules_type,
                                 'unexecuted_module': unexecuted_module, 'task_type': task_type,
                                 'task_status': task_status, 'task_tags': task_tags})


class CaseUpdate(APIView):
    @staticmethod
    def post(request):
        datas = request.data
        print(datas)
        ids, status = [], ''
        for data in datas:
            ids.append(data['id'])
            status = data['status']
        Case.objects.filter(id__in=ids).update(status=status,
                                               update_time=datetime.datetime.now().replace(microsecond=0))
        return APIResponse(code=200, msg='success')


class UploadFile(APIView):
    @staticmethod
    def post(request):
        request_data = request.data
        serCaseList = list(Case.objects.filter(task_id=request.data['id']).values('modules'))
        existCase = []
        for k in serCaseList:
            if k['modules'] not in existCase:
                existCase.append(k['modules'])
        file = openpyxl.load_workbook(request.FILES.get('file'))
        sheet_list = file.get_sheet_names()
        case_data = []
        msg = 'success'
        for i in sheet_list:
            if i[0] != "#":
                sheet = file.get_sheet_by_name(i)
                max = sheet.max_row
                type_name = i
                if type_name in existCase:
                    print(f"检查到重复模块：{type_name} 执行删除操作")
                    Case.objects.filter(modules=type_name).delete()
                for x in range(2, max + 1):
                    try:
                        if sheet["A{}".format(x)].value and sheet["B{}".format(x)].value is not None:
                            assert sheet["D{}".format(x)].value and sheet["E{}".format(x)].value and sheet[
                                "F{}".format(x)].value and sheet["G{}".format(x)].value and sheet[
                                       "J{}".format(x)].value is not None
                            try:
                                assert sheet["I{}".format(x)].value in ('高', '中', '低')
                            except:
                                msg = f"非法优先级规则！ 模块：{i} 第{x}行"
                                return APIResponse(code=200, msg=msg)

                            if "正常" in sheet["H{}".format(x)].value:
                                model = sheet["A{}".format(x)].value
                                model = str(model).replace(r"'", r'"')
                                name = sheet["B{}".format(x)].value
                                name = str(name).replace(r"'", r'"')
                                precondition = sheet["D{}".format(x)].value
                                precondition = str(precondition).replace(r"'", r'"')
                                step = sheet["E{}".format(x)].value
                                step = str(step).replace(r"'", r'"')
                                result = sheet["F{}".format(x)].value
                                result = str(result).replace(r"'", r'"')
                                priority = sheet["I{}".format(x)].value
                                priority = str(priority).replace(r"'", r'"').replace('\n', '')
                                write = sheet["J{}".format(x)].value
                                write = str(write).replace(r"'", r'"')
                                case_data.append(Case(task_id_id=request_data['id'],
                                                      modules=type_name, submodule=model, name=name, steps=step,
                                                      precondition=precondition,
                                                      results=result, priority=priority,
                                                      creator=write, status="未执行"))
                    except Exception as e:
                        msg = f"非法None值！ 模块：{i} 第{x}行"
                        return APIResponse(code=200, msg=msg)
        Case.objects.bulk_create(case_data)
        return APIResponse(code=200, msg=msg)


class AssignCase(APIView):
    @staticmethod
    def get(request):
        task_id = request.query_params.get('id')
        task_grade = TaskInfo.objects.filter(id=task_id).values_list('grade', flat=True).first().split(',')
        modules_name = request.query_params.get('modules_name')
        cases = Case.objects.filter(task_id=task_id, priority__in=task_grade)
        if modules_name:
            cases = cases.filter(modules__contains=modules_name)
        task_modules = cases.values('modules', 'task_id', 'task_id__name', 'performer').annotate(Count('modules'))
        queryset = UserInfo.objects.filter(is_tester=True).all()
        user_list = UserSerializer(queryset, many=True).data
        return APIResponse(code=200, msg='success', data={'task_modules': task_modules, 'user_list': user_list,
                                                          'task_grade': task_grade})

    @staticmethod
    def post(request):
        for item in request.data:
            data = Case.objects.filter(task_id=item['task_id'], modules=item['modules']).update(performer=item['name'])
            print(data)

        return APIResponse(code=200, msg='success')


class CaseOperation(APIView):
    @staticmethod
    def get(request):
        cases = Case.objects.order_by('task_id_id')
        filter_case = FilterByCaseId().filter_queryset(request, cases)
        filter_case = FilterByCaseName().filter_queryset(request, filter_case)
        filter_case = FilterByCaseModule().filter_queryset(request, filter_case)
        filter_case = FilterByCaseSubmodule().filter_queryset(request, filter_case)
        filter_case = FilterByCaseStatus().filter_queryset(request, filter_case)
        filter_case = FilterByCasePriority().filter_queryset(request, filter_case)
        filter_case = FilterByCaseCreator().filter_queryset(request, filter_case)
        filter_case = FilterByCasePerformer().filter_queryset(request, filter_case)
        filter_case = FilterByCaseType().filter_queryset(request, filter_case)
        cases_pagination = CasePagination().paginate_queryset(filter_case, request=request)
        case_items = CaseSerializer(cases_pagination, many=True).data
        modules_type = Case.objects.values('modules').annotate(Count('modules'))
        task_type = Case.objects.values('task_id__name').annotate(Count('task_id__name'))
        status = Case.objects.values('status').annotate(Count('status'))
        priority = Case.objects.values('priority').annotate(Count('priority'))
        creator = Case.objects.values('creator').annotate(Count('creator'))
        performer = Case.objects.values('performer').annotate(Count('performer'))
        update_time = Case.objects.values('update_time').annotate(Count('update_time'))
        queryset = UserInfo.objects.filter(is_tester=True).all()
        user_list = UserSerializer(queryset, many=True).data
        return APIResponse(code=200, msg='success',
                           data={'total': len(filter_case), 'items': case_items, 'modules_type': modules_type,
                                 'task_type': task_type, "status": status, "priority": priority, "creator": creator,
                                 "performer": performer, "update_time": update_time, "user_list": user_list})

    @staticmethod
    def post(request):
        datas = request.data
        ids, performer = [], ''
        print(datas)
        for data in datas:
            ids.append(data['id'])
            performer = data['performer']
        Case.objects.filter(id__in=ids).update(performer=performer)
        return APIResponse(code=200, msg='success')


class AssignCaseOperation(APIView):
    @staticmethod
    def post(request):
        ids = []
        datas = request.data
        performer = set()
        for data in datas:
            ids.append(data['id'])
            performer.add(data['performer'])
        Case.objects.filter(id__in=ids).update(performer=''.join(performer))
        return APIResponse(code=200, msg='success')


class UpdateCaseOperation(APIView):
    @staticmethod
    def post(request):
        ids = []
        datas = request.data
        for data in datas:
            ids.append(data['id'])
        Case.objects.filter(id__in=ids).update(performer=None)
        return APIResponse(code=200, msg='success')


class DeleteCase(APIView):

    @staticmethod
    def post(request, *args):
        ids = []
        datas = request.data
        for data in datas:
            ids.append(data['id'])
        Case.objects.filter(id__in=ids).delete()
        return APIResponse(code=200, msg="success")


class TaskDetails(APIView):
    @staticmethod
    def get(request, *args):
        datas = []
        task_id = request.query_params.get('id')
        resp = list(TaskInfo.objects.filter(id=task_id).values('grade', 'name', 'start_time', 'end_time'))
        grade = [result for result in resp[0]['grade'] if result != ',']
        case_set = Case.objects.filter(task_id=task_id, priority__in=grade)
        case_module, user_list, case_name = {}, [], {}
        not_executed = case_set.filter(status='未执行').values_list('modules', flat=True).distinct()
        executed = case_set.exclude(modules__in=not_executed).values_list('modules', flat=True).distinct()
        for user in case_set.values_list('performer', flat=True).annotate(Count('performer')):
            if user is not None:
                case_module[user] = case_set.filter(performer=user).values('modules').annotate(Count('modules'))
                case_name['FALSE'] = not_executed.filter(performer=user)
                case_name['TRUE'] = executed.filter(performer=user)
                fenpei = case_set.filter(task_id=task_id, priority__in=grade, performer=user).count()
                passed = case_set.filter(status="执行通过", performer=user).count()
                failed = case_set.filter(status="执行失败", performer=user).count()
                expire = case_set.filter(status="需求过期", performer=user).count()
                undone = case_set.filter(status="暂未实现", performer=user).count()
                change = case_set.filter(status="需求变更", performer=user).count()
                unexecuted = case_set.filter(status="未执行", performer=user).count()
                try:
                    rate_result = (passed + failed + expire + undone + change) / fenpei
                    prop_rete = (round(rate_result * 100, 2))
                    if prop_rete == 0.0:
                        raise
                except:
                    prop_rete = 0

                if user in user_list:
                    datas.append({"case_module": list(case_module[user])})
                else:
                    datas.append(
                        {"name": user, "task_name": resp[0]['name'], "case_module": dict(case_name),
                         "prop_rete": str(prop_rete) + '%', "fenpei": fenpei, "passed": passed, "failed": failed,
                         "unexecuted": unexecuted, "expire": expire, "undone": undone, "change": change})
                user_list.append(user)
        start_time = resp[0]['start_time'] + datetime.timedelta(hours=8)
        end_time = resp[0]['end_time'] + datetime.timedelta(hours=8)
        case_sum = case_set.count()
        unassigned = case_set.filter(performer=None).count()
        passed = case_set.filter(status="执行通过").count()
        failed = case_set.filter(status="执行失败").count()
        expire = case_set.filter(status="需求过期").count()
        undone = case_set.filter(status="暂未实现").count()
        change = case_set.filter(status="需求变更").count()
        unexecuted = case_set.filter(status="未执行").count()
        try:
            rate_result = (passed + failed + expire + undone + change) / case_sum
            prop_rete = (round(rate_result * 100, 2))
            if prop_rete == 0.0:
                raise
        except:
            prop_rete = 0
        prop_rete = str(prop_rete) + str('%')
        Overall = [case_sum, unassigned, passed, failed, expire, undone, change, unexecuted, prop_rete]
        return APIResponse(code=200, msg='success',
                           data={'datas': datas, 'start_time': start_time, 'end_time': end_time, 'Overall': Overall})


class UpdateProblemCase(APIView):
    @staticmethod
    def post(request, *args):
        datas = request.data
        id = datas['id']
        remark = datas['remark']
        Case.objects.filter(id=id).update(flag=1, remark=remark)
        return APIResponse(code=200, msg='success')


class QuestionList(APIView):
    @staticmethod
    def get(request, *args):
        cases = Case.objects.filter(flag=1).order_by('-id')
        filter_case = FilterByCaseId().filter_queryset(request, cases)
        filter_case = FilterByCaseName().filter_queryset(request, filter_case)
        filter_case = FilterByCaseModule().filter_queryset(request, filter_case)
        filter_case = FilterByCaseSubmodule().filter_queryset(request, filter_case)
        cases_pagination = CasePagination().paginate_queryset(filter_case, request=request)
        case_items = CaseSerializer(cases_pagination, many=True).data
        modules_type = Case.objects.filter(flag=1).values('modules').annotate(Count('modules'))
        task_type = Case.objects.filter(flag=1).values('task_id__name').annotate(Count('task_id__name'))
        return APIResponse(code=200, msg='success',
                           data={'total': len(filter_case), 'items': case_items, 'modules_type': modules_type,
                                 'task_type': task_type})


class deleteQuestion(APIView):
    @staticmethod
    def delete(request, *args, **kwargs):
        case_id = kwargs['id']
        Case.objects.filter(id=case_id).update(flag=None, remark=None)
        # print(UserInfo.objects.get(id=1).role_name)

        return APIResponse(code=200, msg="success")


class AssignDelete(APIView):
    @staticmethod
    def post(request):
        print(request.data)
        Case.objects.filter(task_id=request.data[0]['task_id'], modules=request.data[0]['modules']).delete()
        return APIResponse(code=200, msg="success")
