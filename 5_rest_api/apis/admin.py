from django.contrib import admin
from .models import School, Teacher, Classroom, Student

# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'address')
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'gender', 'school')
    list_filter = ('school', 'gender')
    search_fields = ('first_name', 'last_name')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'grade', 'room_number', 'teacher_list', 'student_count', 'school')
    list_filter = ('grade', 'school')
    
    def teacher_list(self, obj):
        return ", ".join([t.first_name for t in obj.teachers.all()])
    teacher_list.short_description = 'Teachers'
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'gender', 'classroom', 'school_info')
    list_filter = ('classroom__school', 'classroom', 'gender')
    search_fields = ('first_name', 'last_name')
    
    def school_info(self, obj):
        return obj.classroom.school.name
    school_info.short_description = 'School'