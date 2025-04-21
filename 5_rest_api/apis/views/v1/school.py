from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ...models import School
from ...serializers import SchoolSerializer, SchoolDetailSerializer, SchoolCreateUpdateSerializer
from ...filters import SchoolFilter

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SchoolFilter
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SchoolCreateUpdateSerializer
        return SchoolSerializer