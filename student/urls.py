from django.urls import path
from . import views

urlpatterns = [
    path("",views.index , name ="studenthome"),
    path("register/",views.register, name ="register"),
    path("register_check/",views.register_check,name="register_check"),
    path("studentprofile_form_submission/",views.studentprofile_form_submission,name ="studentprofile_form_submission"),
    path("student_logout/",views.student_logout,name ="student_logout"),

    path("student_course_reg/",views.student_course_reg,name="student_course_reg"),
    path("update_details_student/",views.update_details_student,name="update_details_student"),
    path("course_registration/",views.course_registration,name="course_registration"),
    path("update_details_student_sub/",views.update_details_student_sub,name="update_details_student_sub"),
    path("changepassword_sub/",views.changepassword_sub,name="changepassword_sub"),
    path("change_password_request/",views.change_password_request,name="change_password_request")
]
