from django.urls import path
from . import views,auth

urlpatterns = [
    path("",views.index , name ="login"),
    path("login_submission/",auth.login,name ="login_submission")
]
