from django.db import models


# Create your models here.
class StudentProfile(models.Model):
    first_name =models.CharField(max_length=30,default="")
    last_name =models.CharField(max_length=20)
    email =models.CharField(max_length=40)
    registration_no =models.CharField(max_length=10,primary_key=True)
    password =models.CharField(max_length=35)
    dateofbirth =models.DateField(null=True,blank=False)
    branch =models.CharField(max_length=40)
    gender =models.CharField(max_length=20)
    yearofreg =models.CharField(max_length=10,default="")
    monthofreg =models.CharField(max_length=10)
    def __str__(self):
        return str(self.registration_no)

class StudentCourse(models.Model):
    registration_no=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    course_id = models.CharField(max_length=20)
    course_name =models.CharField(max_length=50)

    year_of_course =models.CharField(max_length=15,default="")
    semester =models.CharField(max_length=15,default="")

    def __str__(self):
        return '{}{}' .format(self.registration_no,self.course_id)
