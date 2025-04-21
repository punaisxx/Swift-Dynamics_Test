from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ...models import Teacher
from ...serializers import TeacherSerializer, TeacherCreateUpdateSerializer
from ...filters import TeacherFilter

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeacherCreateUpdateSerializer
        return TeacherSerializer