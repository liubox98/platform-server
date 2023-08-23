import json
from pypinyin import pinyin, Style
import requests
from rest_framework.decorators import api_view
from modules.commit.models import CommitInfo
from modules.commit.commit_pagination import CommitPagination
from utils.response import APIResponse


# Create your views here.
@api_view(['GET'], )
def commit_list(request):
    version = request.query_params.get('version')
    confire = request.query_params.get('confire')
    isIgnore = request.query_params.get('isIgnore')
    name = request.query_params.get('name')
    if version:
        commit_infos = CommitInfo.objects.filter(version=version).values()
    else:
        commit_infos = CommitInfo.objects.filter().values()
    if confire:
        confire = True if confire == "true" else False
        commit_infos = commit_infos.filter(confire=confire).values()
    if isIgnore:
        isIgnore = True if isIgnore == "true" else False
        commit_infos = commit_infos.filter(isIgnore=isIgnore).values()
    if name:
        commit_infos = commit_infos.filter(name__contains=name).values()
    commit_nums = len(commit_infos)
    version_list = CommitInfo.objects.values_list('version', flat=True).distinct()
    commit_infos = CommitPagination().paginate_queryset(commit_infos, request)
    return APIResponse(code=200, msg="success",
                       data={'items': list(commit_infos), 'version_list': version_list, 'total': commit_nums})


@api_view(['POST'], )
def update_commit_status(request):
    for info in request.data:
        CommitInfo.objects.filter(commit_hash=info['commit_hash']).update(confire=info['confire'])
    return APIResponse(code=200, msg="success")


@api_view(['POST'], )
def upload_commit_file(request):
    file = request.FILES.get('file')
    # 不写文件改写到数据库
    # with open(os.path.join(BASE_DIR, "ReleaseCheck.json"), "wb") as f:
    #     for chunk in file.chunks():
    #         f.write(chunk)
    release_commits = json.loads(file.read(), encoding="utf-8")
    flat_datas = paras_commit_info(release_commits)
    commit_model_objs = []
    for data in flat_datas:
        version, commit_hash, name, detail = data['version'], data['commit_hash'], data['name'], data['detail']
        if not CommitInfo.objects.filter(commit_hash=commit_hash):
            commit_model_objs.append(CommitInfo(version=version, commit_hash=commit_hash, name=name, detail=detail))
    print(commit_model_objs)
    CommitInfo.objects.bulk_create(commit_model_objs)
    return APIResponse(code=200, msg="success", )


def paras_commit_info(data):
    # 获取嵌套结构中的数据
    flat_data = []
    for version, release_data in data.items():
        for commit_hash, value in release_data.items():
            flat_data.append({
                'version': version,
                'commit_hash': commit_hash,
                'name': value['name'],
                'detail': value['detail'],
                'confirm': value['confirm']
            })
    return flat_data


@api_view(['get'], )
def notify_robot(request):
    version = request.query_params.get('version')
    commits_name = list(
        set([commit.name for commit in
             CommitInfo.objects.filter(version=version, confire=False, isIgnore=False).all()]))
    print("需要提醒人员：", commits_name)
    commits_name = list(set([chinese_to_pinyin(name) for name in commits_name]))
    print("转拼音后：", commits_name)
    webhook = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=06e5af3b-b037-459b-a07b-69de6022d12f'
    if commits_name:
        # webhook = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a8528fc7-569f-43d1-a497-7f4bfcb5f0f3'
        headers = {"Content-Type": "application/json"}

        data = {
            "msgtype": "text",
            "text": {
                "content": f"当前版本{version}还有存在未确认的提交，请进入网页确认是否已合并http://novatest.gg.com:8000/#/commit",
                "mentioned_list": commits_name
            }
        }

        res = requests.post(webhook, json=data, headers=headers)
    return APIResponse(code=200, msg="success", )


@api_view(['post'], )
def update_commit_is_ignore_status(request):
    info = request.data
    CommitInfo.objects.filter(commit_hash=info['commit_hash']).update(isIgnore=info['isIgnore'])
    return APIResponse(code=200, msg="success")


def chinese_to_pinyin(chinese_str):
    if chinese_str == '袁晟铭':
        chinese_str = "yuanshengming"
    if chinese_str == "缪宇鑫":
        chinese_str = "miaoyuxin"
    pinyin_list = pinyin(chinese_str, style=Style.NORMAL)
    pinyin_str = ''.join(pinyin_list[i][0].capitalize() for i in range(len(pinyin_list)))
    if pinyin_str:
        pinyin_str = pinyin_str.replace("Yuqi\\", "")
    return pinyin_str
