from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.v1.school import SchoolViewSet
from .views.v1.teacher import TeacherViewSet
from .views.v1.student import StudentViewSet
from .views.v1.classroom import ClassroomViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'students', StudentViewSet, basename='student')

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]
