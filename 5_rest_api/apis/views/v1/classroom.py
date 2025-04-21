from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ...models import Classroom
from ...serializers import ClassroomSerializer, ClassroomCreateUpdateSerializer
from ...filters import ClassroomFilter

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClassroomFilter
    ordering = ['grade', 'room_number']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ClassroomCreateUpdateSerializer
        return ClassroomSerializer