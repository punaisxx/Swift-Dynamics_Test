from django_filters import FilterSet, filters
from .models import School, Teacher, Classroom, Student

# code here
class SchoolFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label="โรงเรียน")
    
    class Meta:
        model = School
        fields = ['name']

class ClassroomFilter(FilterSet):
    school = filters.ModelChoiceFilter(queryset=School.objects.all(), label="โรงเรียน")
    
    class Meta:
        model = Classroom
        fields = ['school']

class TeacherFilter(FilterSet):
    school = filters.ModelChoiceFilter(
        queryset=School.objects.all(),
        label="โรงเรียน"
    )
    classroom = filters.ModelChoiceFilter(
        queryset=Classroom.objects.all(),
        method='filter_by_classroom',
        label="ห้องเรียน"
    )
    first_name = filters.CharFilter(
        lookup_expr='icontains',
        label="ชื่อ"
    )
    last_name = filters.CharFilter(
        lookup_expr='icontains',
        label="นามสกุล"
    )
    gender = filters.ChoiceFilter(
        choices=Teacher.GENDER_CHOICES,
        label="เพศ"
    )
    
    class Meta:
        model = Teacher
        fields = ['school', 'classroom', 'first_name', 'last_name', 'gender']
    
    def filter_by_classroom(self, queryset, name, value):
        return queryset.filter(classrooms=value)

class StudentFilter(FilterSet):
    school = filters.ModelChoiceFilter(
        queryset=School.objects.all(),
        method='filter_by_school',
        label="โรงเรียน"
    )
    classroom = filters.ModelChoiceFilter(queryset=Classroom.objects.all(), label="ห้องเรียน")
    first_name = filters.CharFilter(lookup_expr='icontains', label="ชื่อ")
    last_name = filters.CharFilter(lookup_expr='icontains', label="นามสกุล")
    gender = filters.ChoiceFilter(choices=Student.GENDER_CHOICES, label="เพศ")
    
    class Meta:
        model = Student
        fields = ['classroom', 'first_name', 'last_name', 'gender']
    
    def filter_by_school(self, queryset, name, value):
        return queryset.filter(classroom__school=value)