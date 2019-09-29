from django.urls import path
from . import views

urlpatterns = [
    path("facultyhome/",views.index , name ="facultyhome"),
    path("course_assigned",views.course_assigned,name ="course_assigned"),
    path("last_date_added",views.last_date_added,name="last_date_added"),
    path("mark_entry_home/",views.mark_entry_home,name="mark_entry_home"),
    path("mark_entry_year_sub/",views.mark_entry_year_sub,name="mark_entry_year_sub"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path("change_password_form/",views.change_password_form,name="change_password_form"),
    path("mark_entry/",views.mark_entry,name="mark_entry"),
    path("save_marks/",views.save_marks,name="save_marks"),
    path("faculty_logout/",views.faculty_logout, name= "faculty_logout"),
    path("view_mark_home/",views.view_mark_home,name="view_mark_home"),
    path("view_mark_year_sub/",views.view_mark_year_sub,name="view_mark_year_sub"),
    path("view_mark",views.view_mark,name="view_mark"),
    path("view_mark_entry",views.view_mark_entry,name="view_mark_entry"),
    path("update_details",views.update_details,name="update_details"),
    path("update_details_sub",views.update_details_sub,name="update_details_sub")
]
