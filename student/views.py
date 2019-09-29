from django.shortcuts import render,redirect
from .models import StudentProfile,StudentCourse
from dean.models import AddCourse
from faculty.models import MarksEntry
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

def index(request):
    username = request.session.get('username')
    student_profile = StudentProfile.objects.get(registration_no=username)


    return render(request,'student/student_home_temp.html',{'student':student_profile})
def register(request):
    return render(request,'student/Register.html')
def register_check(request):
    profile_details=dict()
    profile_details['first_name'] = request.POST["first_name"]
    print(profile_details['first_name'])
    profile_details['last_name'] = request.POST["last_name"]
    profile_details['email'] = request.POST["email"]
    profile_details['registration_no'] = request.POST["registration_no"]
    profile_details['password'] = request.POST["password"]

    profile_details['repassword'] = request.POST["re_password"]
    profile_details['dateofbirth'] = request.POST["dateofbirth"]
    profile_details['branch'] = request.POST["branch"]
    profile_details['gender'] = request.POST["gender"]
    profile_details['yearofreg'] = request.POST["year_of_reg"]
    profile_details['monthofreg']= request.POST["month_of_reg"]
    return render(request,'student/register_verify.html',{'profile_details':profile_details})

def studentprofile_form_submission(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    registration_no = request.POST["registration_no"]
    password = request.POST["password"]
    re_password = request.POST["re_password"]
    dateofbirth =request.POST["dateofbirth"]
    branch =request.POST["branch"]
    gender =request.POST["gender"]
    yearofreg =request.POST["year_of_reg"]
    monthofreg=request.POST["month_of_reg"]

    if 'accept'in request.POST:

        length = len(registration_no)
        if length == 10:

            if password == re_password :
                student_profile = StudentProfile(first_name=first_name.title(), last_name=last_name.title(), email=email, registration_no=registration_no, password=password,dateofbirth=dateofbirth ,branch=branch ,gender=gender,yearofreg=yearofreg,monthofreg=monthofreg)
                student_profile.save()
                messages.success(request,"your profile has been created .please login!")
                return redirect('login')
            else:
                messages.error(request ,'Passwords do not match!Try again')
                return redirect(register)
        else:
            messages.error(request, 'Registration number  should have  10 characters')
            return redirect(register)
    else:
        return redirect(register)
def student_logout(request):
    request.session.clear()
    return redirect('login')
def student_course_reg(request):
    courses =AddCourse.objects.all()


    return render(request,'student/student_reg.html',{'courses':courses})

def course_registration(request):
    username = request.session.get('username')
    student_profile = StudentProfile.objects.get(registration_no=username)
    registration_no = student_profile
    course_id = request.POST["course_id"]
    course_name_id = request.POST["course_name"]



    if course_id == course_name_id:
        try:
            student = StudentCourse.objects.get(registration_no=registration_no,course_id=course_id.upper())
            messages.error(request, 'You have already registered for this course! Please try again')
            return redirect('student_course_reg')

        except ObjectDoesNotExist:
            year_of_course = request.POST["year_of_course"]
            semester = request.POST["semester"]
            course=AddCourse.objects.get(course_id=course_id)
            course_reg = StudentCourse(registration_no=registration_no,course_id=course_id.upper(),course_name=course.course_name, year_of_course=year_of_course,semester=semester)
            course_reg.save()
            messages.success(request, 'Course  is registered Successfully!')
            return redirect(student_course_reg)
    else:
        messages.error(request,'Please select valid course name for given  course id!')
        return redirect('student_course_reg')


def update_details_student(request):
    username=request.session.get('username')
    personal_details=StudentProfile.objects.get(registration_no=username)

    dob=personal_details.dateofbirth.strftime("%Y-%m-%d")
    return render(request,'student/update_details.html',{'personal_details':personal_details,'dob':dob})

def update_details_student_sub(request):

    first_name=request.POST['first_name']
    last_name=request.POST['last_name']
    email=request.POST['emailid']
    dob= request.POST['dateofbirth']


    username=request.session.get('username')

    student= StudentProfile.objects.get(registration_no=username)


    if first_name.title() != student.first_name.title() or last_name.title() != student.last_name.title() or email != student.email or dob != str(student.dateofbirth):

        if email != student.email:

            if StudentProfile.objects.filter(email=email).exists():
                error= "Email id is already taken please try again with different email id!!"
                username = request.session.get('username')
                personal_details = StudentProfile.objects.get(registration_no=username)

                dob = personal_details.dateofbirth.strftime("%Y-%m-%d")
                return render(request, 'student/update_details.html',
                              {'personal_details': personal_details, 'dob': dob, 'error': error})

            else:
                StudentProfile.objects.filter(registration_no=username).update(email=email)
                


        if first_name.title() != student.first_name.title():
            StudentProfile.objects.filter(registration_no=username).update(first_name=first_name)

        if last_name.title() != student.last_name.title():
            StudentProfile.objects.filter(registration_no=username).update(last_name=last_name)

        if dob != str(student.dateofbirth):
            StudentProfile.objects.filter(registration_no=username).update(dateofbirth=dob)


        success="Your provided details is updated!"
        username = request.session.get('username')
        personal_details = StudentProfile.objects.get(registration_no=username)

        dob = personal_details.dateofbirth.strftime("%Y-%m-%d")
        return render(request,'student/update_details.html',{'personal_details': personal_details, 'dob': dob,'success':success})

    else:
        username = request.session.get('username')
        personal_details = StudentProfile.objects.get(registration_no=username)

        dob = personal_details.dateofbirth.strftime("%Y-%m-%d")
        error = "No details are updated!!"
        return render(request, 'student/update_details.html', {'personal_details': personal_details, 'dob': dob,'error':error})

def changepassword_sub(request):
    return render(request,"student/changepassword.html")

def change_password_request(request):
    oldpassword = request.POST["oldpassword"]
    newpassword = request.POST["newpassword"]
    renewpassword = request.POST["renewpassword"]
    username = request.session.get('username')
    faculty_instance = StudentProfile.objects.get(registration_no=username)
    if faculty_instance.password == oldpassword:
        if newpassword == renewpassword:
            StudentProfile.objects.filter(registration_no=username, password=oldpassword).update(password=newpassword)
            success = "Password changed successfully!"
            return render(request, "student/changepassword.html", {'success': success})
        else:
            error = "New Password field do not match with Retype New Password field!"
            return render(request, "student/changepassword.html", {'error': error})
    else:
        error = "Please enter right password!!"
        return render(request, "student/changepassword.html", {'error': error})
