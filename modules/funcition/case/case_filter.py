from rest_framework.filters import BaseFilterBackend


class FilterByCaseId(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('id')
        if query:
            return queryset.filter(id__contains=query)
        else:
            return queryset


class FilterByCaseName(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('task_name')
        if query:
            return queryset.filter(task_id__name=query)
        else:
            return queryset


class FilterByCaseModule(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('modules')
        if query:
            return queryset.filter(modules=query)
        else:
            return queryset


class FilterByCaseUnexecutedModule(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('unexecuted_modules')
        if query:
            return queryset.filter(modules=query)
        else:
            return queryset


class FilterByCaseSubmodule(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('submodule')
        if query:
            return queryset.filter(submodule__contains=query)
        else:
            return queryset


class FilterByCaseStatus(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('status')
        if query:
            return queryset.filter(status__contains=query)
        else:
            return queryset


class FilterByCasePriority(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('priority')
        if query:
            return queryset.filter(priority__contains=query)
        else:
            return queryset


class FilterByCaseCreator(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('creator')
        if query:
            return queryset.filter(creator__contains=query)
        else:
            return queryset


class FilterByCasePerformer(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('performer')
        if query:
            return queryset.filter(performer__contains=query)
        else:
            return queryset


class FilterByCaseType(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view=None):
        query = request.query_params.get('type')
        if query:
            return queryset.filter(type__contains=query)
        else:
            return queryset
