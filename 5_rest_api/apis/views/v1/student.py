from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ...models import Student
from ...serializers import StudentSerializer, StudentCreateUpdateSerializer
from ...filters import StudentFilter

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    ordering = ['classroom__grade', 'classroom__room_number', 'last_name', 'first_name']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentCreateUpdateSerializer
        return StudentSerializer