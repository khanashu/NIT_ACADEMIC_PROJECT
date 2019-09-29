from django.contrib import admin

from .models import FacultyCredential,StudentCredential

admin.site.register(StudentCredential)
admin.site.register(FacultyCredential)
