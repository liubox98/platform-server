from rest_framework.pagination import PageNumberPagination


# 自动化分页配置
class AutoPagination(PageNumberPagination):
    # 默认第几页
    page_size = 1
    # 每页最大显示条数
    max_page_size = 50
    # 查询条件为？page={page}&limit={limit}
    page_query_param = 'page'
    page_size_query_param = 'limit'
