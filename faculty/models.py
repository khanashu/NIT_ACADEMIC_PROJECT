from django.db import models
from student.models import StudentProfile
from dean.models import AddFaculty

# Create your models here.
class MarksEntry(models.Model):
    registration_no=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    mid_sem= models.IntegerField(default=0)
    end_sem = models.IntegerField(default=0)
    course_id=models.CharField(max_length=20)
    year=models.CharField(max_length=20)
    semester=models.CharField(max_length=12)
    total_marks=models.IntegerField(default=0)
    Grade=models.CharField(max_length=5)
    Accepted=models.CharField(max_length=2,default=0)

    def __str__(self):
        return '{}{}'.format(self.course_id, self.registration_no)

class FacultyNotifications(models.Model):
    employee_code=models.ForeignKey(AddFaculty, on_delete=models.CASCADE)
    course_id=models.CharField(max_length=10)
    year=models.CharField(max_length=14)
    semester=models.CharField(max_length=12)
    read=models.CharField(max_length=2,default=0)
    accepted=models.CharField(max_length=2,default=0)

    def __str__(self):
        return '{}{}'.format(self.employee_code,self.course_id)
