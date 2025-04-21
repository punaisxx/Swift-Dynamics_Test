from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import School, Teacher, Classroom, Student

# Create your tests here.
class SchoolAPITestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test1234'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client = APIClient()
        self.client.login(username=self.username, password=self.password)
        
        self.school_data = {
            'name': 'โรงเรียนนกกระทุง',
            'abbreviation': 'นกท.',
            'address': '123 ถนนกระทุง เขาใหญ่'
        }
        self.school = School.objects.create(**self.school_data)
        self.url = '/api/v1/schools/'
        self.detail_url = f'/api/v1/schools/{self.school.pk}/'

    def test_get_all_schools(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_school(self):
        new_school_data = {
            'name': 'โรงเรียนไก่แจ้',
            'abbreviation': 'กจ.',
            'address': '123 ถนนไก่ไก่ เขาใหญ่'
        }
        response = self.client.post(self.url, new_school_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 2)

    def test_get_single_school(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.school_data['name'])

    def test_update_school(self):
        update_data = {'name': 'โรงเรียนไก่แจ้2'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'โรงเรียนไก่แจ้2')

    def test_delete_school(self):
      response = self.client.delete(self.detail_url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)  
      self.assertEqual(School.objects.count(), 0)

    def test_filter_school_by_name(self):
        School.objects.create(name='โรงเรียนลามาเซีย', abbreviation='ลมซ.', address='24/7 บาร์เซโลนา')
        
        response = self.client.get(f"{self.url}?name=ลาม")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'โรงเรียนลามาเซีย')

class TeacherAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.username = 'test'
        self.password = 'test1234'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client.login(username=self.username, password=self.password)
        
        self.school = School.objects.create(name='โรงเรียนเต่าทอง', abbreviation='รท')
        
        self.teacher_data = {
            'first_name': 'จอห์น',
            'last_name': 'เลนนอน',
            'gender': 'ชาย',
            'school': self.school.id
        }
        
        self.teacher = Teacher.objects.create(**{
            'first_name': self.teacher_data['first_name'],
            'last_name': self.teacher_data['last_name'],
            'gender': self.teacher_data['gender'],
            'school': self.school
        })
        
        self.url = '/api/v1/teachers/'
        self.detail_url = f'/api/v1/teachers/{self.teacher.pk}/'

    def test_get_all_teachers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_teacher(self):
        new_teacher_data = {
            'first_name': 'จอร์จ',
            'last_name': 'ฮาริสัน',
            'gender': 'ชาย',
            'school': self.school.id
        }
        response = self.client.post(self.url, new_teacher_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 2)

    def test_get_single_teacher(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.teacher_data['first_name'])
        self.assertEqual(response.data['last_name'], self.teacher_data['last_name'])

    def test_update_teacher(self):
        update_data = {'first_name': 'จอห์นนี่'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'จอห์นนี่')

    def test_delete_teacher(self):
        initial_count = Teacher.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(Teacher.objects.count(), initial_count - 1)
        
        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(pk=self.teacher.pk)

    def test_filter_teacher_by_school(self):
        school2 = School.objects.create(name='โรงเรียนเต่าทอง2')
        Teacher.objects.create(
            first_name='พอล',
            last_name='แม็กคาร์ทนีย์',
            gender='ชาย',
            school=school2
        )
        
        response = self.client.get(f"{self.url}?school={self.school.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['first_name'], self.teacher_data['first_name'])
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['first_name'], self.teacher_data['first_name'])


class ClassroomAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.username = 'test'
        self.password = 'test1234'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client.login(username=self.username, password=self.password)
        
        self.school = School.objects.create(name='โรงเรียนทดสอบ', abbreviation='รท')
        self.teacher = Teacher.objects.create(
            first_name='จอห์น',
            last_name='จอห์นนี่',
            gender='ชาย',
            school=self.school
        )
        
        self.classroom_data = {
            'grade': 1,
            'room_number': '1',
            'school': self.school.id,
            'teachers': [self.teacher.id]
        }
        
        self.classroom = Classroom.objects.create(
            grade=self.classroom_data['grade'],
            room_number=self.classroom_data['room_number'],
            school=self.school
        )
        self.classroom.teachers.add(self.teacher)
        
        self.url = '/api/v1/classrooms/'
        self.detail_url = f'/api/v1/classrooms/{self.classroom.pk}/'

    def test_get_all_classrooms(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1) 
        else:
            self.assertEqual(len(response.data), 1)

    def test_create_classroom(self):
        new_classroom_data = {
            'grade': 2,
            'room_number': '1',
            'school': self.school.id,
            'teachers': [self.teacher.id]
        }
        response = self.client.post(self.url, new_classroom_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 2)

    def test_get_single_classroom(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['grade'], self.classroom_data['grade'])
        self.assertEqual(response.data['room_number'], self.classroom_data['room_number'])

    def test_update_classroom(self):
        update_data = {'room_number': '8'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['room_number'], '8')

    def test_delete_classroom(self):
        initial_count = Classroom.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Classroom.objects.count(), initial_count - 1)
        
        with self.assertRaises(Classroom.DoesNotExist):
            Classroom.objects.get(pk=self.classroom.pk)

    def test_filter_classroom_by_school(self):
        school2 = School.objects.create(name='โรงเรียนเต่าทอง2')
        classroom2 = Classroom.objects.create(
            grade=1,
            room_number='1',
            school=school2
        )
        
        response = self.client.get(f"{self.url}?school={self.school.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['grade'], self.classroom_data['grade'])
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['grade'], self.classroom_data['grade'])


class StudentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.username = 'test'
        self.password = 'test1234'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client.login(username=self.username, password=self.password)
        
        self.school = School.objects.create(name='โรงเรียนเต่าทะเล', abbreviation='รท')
        self.classroom = Classroom.objects.create(
            grade=1,
            room_number='1',
            school=self.school
        )
        
        self.student_data = {
            'first_name': 'ริงโก้',
            'last_name': 'สตาร์',
            'gender': 'ชาย',
            'classroom': self.classroom.id
        }
        
        self.student = Student.objects.create(
            first_name=self.student_data['first_name'],
            last_name=self.student_data['last_name'],
            gender=self.student_data['gender'],
            classroom=self.classroom
        )
        
        self.url = '/api/v1/students/'
        self.detail_url = f'/api/v1/students/{self.student.pk}/'

    def test_get_all_students(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_create_student(self):
        new_student_data = {
            'first_name': 'บิลลี่',
            'last_name': 'โจ',
            'gender': 'ชาย',
            'classroom': self.classroom.id
        }
        response = self.client.post(self.url, new_student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_get_single_student(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.student_data['first_name'])
        self.assertEqual(response.data['last_name'], self.student_data['last_name'])

    def test_update_student(self):
        update_data = {'first_name': 'ลิ้นจี่'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'ลิ้นจี่')

    def test_delete_student(self):
        initial_count = Student.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.count(), initial_count - 1)
        
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=self.student.pk)

    def test_filter_student_by_classroom(self):
        classroom2 = Classroom.objects.create(
            grade=2,
            room_number='1',
            school=self.school
        )
        student2 = Student.objects.create(
            first_name='ไมค์',
            last_name='เดินต์',
            gender='ชาย',
            classroom=classroom2
        )
        
        response = self.client.get(f"{self.url}?classroom={self.classroom.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['first_name'], self.student_data['first_name'])
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['first_name'], self.student_data['first_name'])

    def test_filter_student_by_school(self):
        school2 = School.objects.create(name='โรงเรียนเต่ามะเฟือง')
        classroom2 = Classroom.objects.create(
            grade=1,
            room_number='1',
            school=school2
        )
        student2 = Student.objects.create(
            first_name='ทรี',
            last_name='คูล',
            gender='ชาย',
            classroom=classroom2
        )
        
        response = self.client.get(f"{self.url}?school={self.school.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['first_name'], self.student_data['first_name'])
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['first_name'], self.student_data['first_name'])