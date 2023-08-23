from rest_framework.pagination import PageNumberPagination


# 任务分页配置
class TaskPagination(PageNumberPagination):
    # 默认第几页
    page_size = 1
    # 默认每页显示条数
    max_page_size = 10
    # 查询条件为？page={page}&limit={limit}
    page_query_param = 'page'
    page_size_query_param = 'limit'
