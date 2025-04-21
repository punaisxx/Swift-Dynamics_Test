from rest_framework import serializers
from .models import School, Teacher, Classroom, Student

# code here
class StudentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender']


class TeacherSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender']


class ClassroomSimpleSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source='school.name')
    
    class Meta:
        model = Classroom
        fields = ['id', 'grade', 'room_number', 'school_name']


class SchoolSerializer(serializers.ModelSerializer):
    classrooms_count = serializers.SerializerMethodField()
    teachers_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = School
        fields = ['id', 'name', 'abbreviation', 'address', 'classrooms_count', 'teachers_count', 'students_count']
    
    def get_classrooms_count(self, obj):
        return obj.classrooms.count()
    
    def get_teachers_count(self, obj):
        return obj.teachers.count()
    
    def get_students_count(self, obj):
        students_count = 0
        for classroom in obj.classrooms.all():
            students_count += classroom.students.count()
        return students_count


class TeacherSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source='school.name')
    classrooms = ClassroomSimpleSerializer(many=True, read_only=True)  
    
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'school', 'school_name', 'classrooms']

class ClassroomSerializer(serializers.ModelSerializer):
    teachers = TeacherSimpleSerializer(many=True, read_only=True)
    students = StudentSimpleSerializer(many=True, read_only=True)
    school = serializers.StringRelatedField(read_only=True)
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Classroom
        fields = ['id', 'grade', 'room_number', 'school', 'teachers', 'students', 'students_count']
    
    def get_students_count(self, obj):
        return obj.students.count()


class ClassroomListSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source='school.name')
    teachers_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Classroom
        fields = ['id', 'grade', 'room_number', 'school_name', 'teachers_count', 'students_count']
    
    def get_teachers_count(self, obj):
        return obj.teachers.count()
    
    def get_students_count(self, obj):
        return obj.students.count()


class ClassroomDetailSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source='school.name')
    teachers = TeacherSimpleSerializer(many=True, read_only=True) 
    students = StudentSimpleSerializer(many=True, read_only=True, source='students.all') 
    students_count = serializers.SerializerMethodField()
    teachers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Classroom
        fields = ['id', 'grade', 'room_number', 'school_name', 'teachers_count', 'teachers', 'students_count', 'students']
    
    def get_students_count(self, obj):
        return obj.students.count()
        
    def get_teachers_count(self, obj):
        return obj.teachers.count()


class StudentSerializer(serializers.ModelSerializer):
    classroom_info = serializers.SerializerMethodField()
    school_info = serializers.ReadOnlyField(source='classroom.school.name')
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom', 'classroom_info', 'school_info']
    
    def get_classroom_info(self, obj):
        return f"ชั้นปีที่ {obj.classroom.grade}/{obj.classroom.room_number}"

class SchoolDetailSerializer(serializers.ModelSerializer):
    teachers = TeacherSimpleSerializer(many=True, read_only=True) 
    classrooms = ClassroomListSerializer(many=True, read_only=True)
    classrooms_count = serializers.SerializerMethodField()
    teachers_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = School
        fields = ['id', 'name', 'abbreviation', 'address', 'classrooms_count', 'teachers_count', 'students_count', 'teachers', 'classrooms']
    
    def get_classrooms_count(self, obj):
        return obj.classrooms.count()
    
    def get_teachers_count(self, obj):
        return obj.teachers.count()
    
    def get_students_count(self, obj):
        from django.db.models import Count
        return Student.objects.filter(classroom__school=obj).count()

class TeacherDetailSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source='school.name')
    classrooms = ClassroomListSerializer(many=True, read_only=True)  
    
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'school_name', 'classrooms']

class StudentDetailSerializer(serializers.ModelSerializer):
    classroom_detail = ClassroomSimpleSerializer(source='classroom', read_only=True)
    school_info = serializers.ReadOnlyField(source='classroom.school.name')
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom', 'classroom_detail', 'school_info']

        

class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom']

class TeacherCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'school' ]

class ClassroomCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'grade', 'room_number', 'teachers', 'school']


class SchoolCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'abbreviation', 'address']