from django.contrib import admin

from .models import AddFaculty, AddCourse, AssignTeacher,DeanUser,DeanNotifications,LastDate
# Register your models here.

admin.site.register(AddFaculty)
admin.site.register(AddCourse)
admin.site.register(AssignTeacher)
admin.site.register(DeanUser)
admin.site.register(DeanNotifications)
admin.site.register(LastDate)