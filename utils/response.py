from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, code=100, msg=None, data=None, status=None, template_name=None, headers=None, exception=False,
                 content_type=None, **kwargs):
        dic = {'code': code, 'msg': msg}
        if data:
            dic['data'] = data
        if kwargs:
            dic.update(kwargs)

        super().__init__(data=dic, status=status, template_name=template_name, headers=headers, exception=exception,
                         content_type=content_type)
