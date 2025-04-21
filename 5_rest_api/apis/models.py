from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField("ชื่อโรงเรียน", max_length=200)
    abbreviation = models.CharField("ตัวย่อชื่อโรงเรียน", max_length=30, blank=True)
    address = models.TextField("ที่อยู่", blank=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "โรงเรียน"
        verbose_name_plural = "โรงเรียน"
        
class Teacher(models.Model):
    GENDER_CHOICES = [
        ('ชาย', 'ชาย'),
        ('หญิง', 'หญิง'),
        ('อื่นๆ', 'อื่นๆ'),
    ]
    first_name = models.CharField("ชื่อ", max_length=100)
    last_name = models.CharField("นามสกุล", max_length=100)
    gender = models.CharField("เพศ", max_length=10, choices=GENDER_CHOICES) 
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="teachers")
    
    def __str__(self): 
        return f"{self.first_name} {self.last_name}"
        
    class Meta:
        verbose_name = "คุณครู"
        verbose_name_plural = "คุณครู"
        
class Classroom(models.Model):
    GRADE_CHOICES = [
        (1, 'ชั้นปีที่ 1'),
        (2, 'ชั้นปีที่ 2'),
        (3, 'ชั้นปีที่ 3'),
        (4, 'ชั้นปีที่ 4'),
        (5, 'ชั้นปีที่ 5'),
        (6, 'ชั้นปีที่ 6'),
    ]
    grade = models.IntegerField("ชั้นปี", choices=GRADE_CHOICES)
    room_number = models.CharField("ทับ", max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classrooms")
    teachers = models.ManyToManyField(Teacher, related_name="classrooms")
    
    def __str__(self): 
        return f"{self.grade}/{self.room_number}"
        
    class Meta:
        verbose_name = "ห้องเรียน"
        verbose_name_plural = "ห้องเรียน"
        unique_together = ('grade', 'room_number', 'school')
        
class Student(models.Model):
    GENDER_CHOICES = [
        ('ชาย', 'ชาย'),
        ('หญิง', 'หญิง'),
        ('อื่นๆ', 'อื่นๆ'),
    ]
    first_name = models.CharField("ชื่อ", max_length=100)
    last_name = models.CharField("นามสกุล", max_length=100)
    gender = models.CharField("เพศ", max_length=10, choices=GENDER_CHOICES)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="students")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    class Meta:
        verbose_name = "นักเรียน"
        verbose_name_plural = "นักเรียน"