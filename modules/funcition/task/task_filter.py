from rest_framework.filters import BaseFilterBackend


# class FilterByTaskId(BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view=None):
#         query = request.query_params.get('id')
#         if query:
#             return queryset.filter(id__contains=query)
#         else:
#             return queryset


class FilterByTaskName(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('task_name')
        if query:
            return queryset.filter(name__contains=query)
        else:
            return queryset


class FilterByTaskCreator(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('task_creator')
        if query:
            return queryset.filter(creator__contains=query)
        else:
            return queryset
