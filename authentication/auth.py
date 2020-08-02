from django.shortcuts import  redirect
from .models import StudentCredential, FacultyCredential
from student.models import StudentProfile
from dean.models import AddFaculty,DeanUser
from django.contrib import messages


def login(request):
    username_entered = request.POST.get('username')
    password_entered = request.POST.get('password')

    user_type = None
    if len(username_entered) == 10:

        try:

            user_instance = StudentProfile.objects.get(registration_no=username_entered)
            user_type = 'student'
        except StudentProfile.DoesNotExist:
            messages.error(request ,'Invalid Username! Try Again')
            return redirect('login')
    elif len(username_entered) == 7:

        try:
            user_instance = DeanUser.objects.get(username=username_entered)
            user_type = 'dean'

        except DeanUser.DoesNotExist:
            messages.error(request,'Invalid Username! Try Again')
            return redirect('login')
    else:

        try:
            user_instance = AddFaculty.objects.get(employee_code=username_entered)
            user_type = 'faculty'
        except AddFaculty.DoesNotExist:
            messages.error(request, 'Invalid Username!Try Again')
            return redirect('login')

    if user_instance.password == password_entered:
        request.session['username'] = username_entered
        request.session['logged'] = True
        request.session['user_type'] = user_type
        request.session.set_expiry(0)
        return redirect('login')
    else:
        messages.error(request, 'Wrong Password!Try Again')
        return redirect('login')