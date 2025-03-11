from urllib import request
from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter
from task.models.task import UserTask
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from task.serializers.task import SearchUserTaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from task.utils import SearchPagination
from django.db.models import Q


class UserTaskFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='icontains')
    created_by = filters.CharFilter(field_name='created_by__name', lookup_expr='icontains')
    assigned_to = filters.CharFilter(field_name='assigned_to__name', lookup_expr='icontains')
    desc = filters.CharFilter(field_name='desc', lookup_expr='icontains')
    deadline = DateFromToRangeFilter(field_name='deadline')
    completed_on = DateFromToRangeFilter(field_name='completed_on')
    created_on = DateFromToRangeFilter(field_name='created_on')

    class Meta:
        model = UserTask
        fields = {
            'id': ['exact'],
            'created_by__name': ['exact', 'icontains'],
            'assigned_to__name': ['exact', 'icontains'],
            'desc': ['exact', 'icontains'],
            'created_on': ['exact', 'range'],
            'deadline': ['exact', 'range'],
            'completed_on': ['exact', 'range'],
            'status': ['exact', 'icontains']
        }



class UserTaskSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserTask.objects.all()
    serializer_class = SearchUserTaskSerializer
    filterset_class = UserTaskFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = SearchPagination

    def get_queryset(self):
        user = self.request.user
        ordering = self.request.query_params.get('ordering', 'id')
        queryset = UserTask.objects.filter(
            Q(assigned_to=user) | Q(created_by=user)
        ).select_related('created_by', 'assigned_to')

        return queryset.order_by(ordering)

        