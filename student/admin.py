from django.contrib import admin
from .models import StudentProfile,StudentCourse


# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(StudentCourse)