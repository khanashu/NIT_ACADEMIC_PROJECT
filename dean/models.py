from django.db import models

# Create your models here.

class AddFaculty(models.Model):
    first_name = models.CharField(max_length=30,default="")
    last_name = models.CharField(max_length=20)

    email = models.CharField(max_length=40)
    employee_code = models.CharField(max_length=10,primary_key=True)
    password = models.CharField(max_length=40)

    dob = models.DateField(null=True, blank=False)
    department = models.CharField(max_length=40)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.employee_code

class AddCourse(models.Model):
    course_id = models.CharField(max_length=20,primary_key=True)
    course_name = models.CharField(max_length=50)
    credits = models.CharField(max_length=6)

    department = models.CharField(max_length=50)

    def __str__(self):
        return self.course_id

class AssignTeacher(models.Model):
    course_id = models.ForeignKey(AddCourse, on_delete=models.CASCADE)

    employee_code = models.ForeignKey(AddFaculty, on_delete=models.CASCADE)

    year_of_assign = models.CharField(max_length=20,default="")
    semester = models.CharField(max_length=20,default="")

    def __str__(self):
        return '{}{}'.format(self.course_id, self.employee_code)
class DeanUser(models.Model):
    username= models.CharField(max_length=8)
    password= models.CharField(max_length=25)

    def __str__(self):
        return self.username
class DeanNotifications(models.Model):

    year=models.CharField(max_length=10)
    course_id=models.CharField(max_length=10)
    semester=models.CharField(max_length=15)

    def __str__(self):
        return '{}{}{}' .format(self.course_id,self.year,self.semester)
class LastDate(models.Model):
    year=models.CharField(max_length=10)
    semester=models.CharField(max_length=15)
    date=models.DateField(null=True,blank=False)

    def __str__(self):
        return '{}{}{}'.format(self.year,self.semester,self.date)