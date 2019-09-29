
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="deanhome"),
    path("dean_evaluative_check/",views.dean_evaluative_check,name="dean_evaluative_check"),

    path("evaluation_home/",views.evaluation_home,name="evaluation_home"),
    path("evaluation_year_sub/",views.evaluation_year_sub,name="evaluation_year_sub"),
    path("evaluation/",views.evaluation,name="evaluation"),
    path("dean_verdict/",views.dean_verdict,name="dean_verdict"),
    path("addfaculty/", views.addfaculty, name="addfaculty"),
    path("add_faculty_form_submission/", views.add_faculty_form_submission, name="add_faculty_form_submission"),
    path("dean_logout/",views.dean_logout,name ="dean_logout"),
    path("addcourse/", views.addcourse, name="addcourse"),
    path("add_course_form_submission/", views.add_course_form_submission, name="add_course_form_submission"),
    path("assign/", views.assign, name="assign"),
    path("assign_teacher_form_submission/", views.assign_teacher_form_submission, name="assign_teacher_form_submission"),
    path("grade_card_generate/",views.grade_card_generate,name="grade_card_generate"),
    path("grade_card/", views.grade_card, name="grade_card"),
    path("last_date_mark/",views.last_date_mark,name="last_date_mark"),
    path("last_date_mark_submission/",views.last_date_mark_submission,name="last_date_mark_submission"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path("changepasswordsubmission/",views.changepasswordsubmission,name="changepasswordsubmission"),
    path("report_home/",views.report_home,name="report_home"),
    path("report_sub/",views.report_sub,name="report_sub"),


]
