from django.db import models


class StudentCredential(models.Model):
    registration_no = models.OneToOneField('student.StudentProfile', on_delete=models.CASCADE)
    password = models.CharField(max_length=30, null=False)

    def __str__(self):
        return str(self.registration_no)


class FacultyCredential(models.Model):
    employee_code = models.OneToOneField('dean.AddFaculty', on_delete=models.CASCADE)
    password = models.CharField(max_length=30, null=False)

    def __str__(self):
    	return str(self.employee_code)