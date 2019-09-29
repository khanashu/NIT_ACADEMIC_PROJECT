from django.shortcuts import render,redirect
from dean.models import AddFaculty,AssignTeacher,AddCourse,DeanNotifications,LastDate
from .models import MarksEntry,FacultyNotifications

from django.contrib import messages
from student.models import StudentCourse,StudentProfile
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    username = request.session.get('username')
    teacher_profile = AddFaculty.objects.get(employee_code=username)
    accepted=FacultyNotifications.objects.filter(employee_code=username,accepted=1)
    rejected=FacultyNotifications.objects.filter(employee_code=username,accepted=0)
    if accepted.count()==0 and rejected.count()==0:
        message="No new notifications are there to show"
        return render(request, 'faculty/facultyhome.html',{'teacher': teacher_profile, 'accepted': accepted, 'rejected': rejected,'message':message})
    else:
        return render(request, 'faculty/facultyhome.html',{'teacher':teacher_profile,'accepted':accepted,'rejected':rejected})

def faculty_logout(request):
    username=request.session.get('username')
    FacultyNotifications.objects.filter(employee_code=username).delete()
    request.session.clear()
    return redirect('login')
def last_date_added(request):
    year = request.POST["year"]
    semester = request.POST["semester"]


    username = request.session.get('username')
    teacher_profile = AddFaculty.objects.get(employee_code=username)
    try:
        last_date_given = LastDate.objects.get(year=year, semester=semester)
        last_date=last_date_given.date.strftime("%d/%m/%Y")
        return render(request, 'faculty/facultyhome.html', {'teacher': teacher_profile, 'last_date': last_date})

    except ObjectDoesNotExist:
        last = "Last date of mark submission will be updated soon!!"
        return render(request, 'faculty/facultyhome.html', {'teacher': teacher_profile, 'last': last})

def course_assigned(request):
    year = request.POST["year"]
    semester = request.POST["semester"]
    username = request.session.get('username')
    teacher_assign = AssignTeacher.objects.filter(employee_code=username,year_of_assign=year,semester=semester)
    obj = teacher_assign.count()
    teacher_profile = AddFaculty.objects.get(employee_code=username)
    if obj ==0:
        messages.error(request, 'No courses have been allotted according to the given year and semester')
        return  render (request,'faculty/facultyhome.html',{'teacher':teacher_profile})
    else:

        messages.success(request,'The allotted courses are as follows')

        return render (request,'faculty/facultyhome.html',{'teacher_assigned':teacher_assign,'teacher':teacher_profile})

def mark_entry_home(request):

        return render(request, 'faculty/mark_entry_home.html')

def mark_entry_year_sub(request):
    year = request.POST["year"]
    semester = request.POST["semester"]
    username = request.session.get('username')
    teacher_assign = AssignTeacher.objects.filter(employee_code=username, year_of_assign=year, semester=semester)
    obj = teacher_assign.count()

    if obj == 0:
        messages.error(request, 'No courses have been allotted according to the given year and semester')
        return render(request, 'faculty/mark_entry_home.html',{} )
    else:

        return render(request, 'faculty/mark_entry_selection.html', {'teacher_assigned': teacher_assign})

def mark_entry(request):
    course_info = request.POST["course_info"]
    course_id = str(course_info)[:6]
    year = str(course_info)[6:15]
    semester =str(course_info)[15:]

    if MarksEntry.objects.filter(course_id=course_id,year=year,semester=semester).exists():
            error ='Marks entry is submitted for this course already!!Please try again with different course'
            return render(request,"faculty/mark_entry_home.html",{'error':error})
    else:
        course_names = AddCourse.objects.get(course_id=course_id)
        course_name = course_names.course_name
        print(course_name)
        students = StudentCourse.objects.filter(course_name=course_name)
        obj = students.count()
        if obj ==0:
            messages.error(request, 'No student has registered for this course')
            return render(request,'faculty/mark_entry_home.html',)
        else:
            return render(request,'faculty/mark_entry.html',{'students':students,'course_id':course_id,'year':year,'semester':semester})


def save_marks(request):
        year,semester,course_id,error= save_marks_in_db(parse_mark_entry(request.POST))
        if error==0:
            error="The mark entry is wrong as either mid sem or end sem mark entry is wrong!!"
            return render(request, 'faculty/mark_entry_home.html', {'error': error})
        else:
            notifications=DeanNotifications.objects.create(year=year,course_id=course_id,semester=semester)
            notifications.save()
            try:
                FacultyNotifications.objects.get(course_id=course_id,year=year,semester=semester).exists()
                FacultyNotifications.objects.get(course_id=course_id,year=year,semester=semester).delete()
            except:
                pass
            success='Marks have been submitted for '+course_id+' for '+semester+ ' of session ' + year
            return render(request,'faculty/mark_entry_home.html',{'success':success})


def parse_mark_entry(post_array):

    print(post_array)
    new_mark_entry = dict()
    new_mark_entry['year'] = post_array.get('year')
    
    new_mark_entry['semester'] = post_array.get('semester')
    new_mark_entry['course_id']=post_array.get('course_id')
    course_id = new_mark_entry['course_id']
    course_name = AddCourse.objects.get(course_id=course_id).course_name
    print(course_name)
    students = StudentCourse.objects.filter(course_name=course_name)

    mark_list = []
    single_student_mark_entered = dict()
    for student in students:
        current_roll=student.registration_no.registration_no


        single_student_mark_entered['reg_no'] = post_array.get('marks_reg' + current_roll)
        single_student_mark_entered['error'] = 0
        single_student_mark_entered['midsem'] = int(post_array.get('marks_midsem' + current_roll))
        single_student_mark_entered['endsem'] = int(post_array.get('marks_endsem' + current_roll))
        if single_student_mark_entered['midsem'] > 50 or single_student_mark_entered['endsem'] > 100:
            single_student_mark_entered['error'] = 1
        single_student_mark_entered['grade']  = post_array.get('marks_grade'+ current_roll).upper()
        mark_list.append(single_student_mark_entered.copy())



    new_mark_entry['students'] = mark_list
    return new_mark_entry


def save_marks_in_db(new_mark_entry):
        year = new_mark_entry.get('year')
        semester = new_mark_entry.get('semester')
        course_id = new_mark_entry.get('course_id')

        for student in new_mark_entry.get('students'):
                reg_no= student['reg_no']
                registration_no =StudentProfile.objects.get(registration_no=reg_no)
                total_marks = student['midsem'] + student['endsem']
                if int(student['error'])==1:
                    return year,semester,course_id,0
                else:
                    mark_entry_of_each_student=MarksEntry.objects.create(registration_no=registration_no,mid_sem=student['midsem'],end_sem=student['endsem'],total_marks=total_marks,Grade=student['grade'].upper(),year=year,semester=semester,course_id=course_id)
                    mark_entry_of_each_student.save()

        return year,semester,course_id,1
def changepassword(request):
    return render(request,"faculty/changepassword.html")

def change_password_form(request):
    oldpassword = request.POST["oldpassword"]
    newpassword = request.POST["newpassword"]
    renewpassword = request.POST["renewpassword"]
    username = request.session.get('username')
    faculty_instance = AddFaculty.objects.get(employee_code=username)
    if faculty_instance.password == oldpassword:
        if newpassword == renewpassword:
            AddFaculty.objects.filter(employee_code=username, password=oldpassword).update(password=newpassword)
            success = "Password changed successfully!"
            return render(request, "faculty/changepassword.html", {'success': success})
        else:
            error = "New Password field do not match with Retype New Password field!"
            return render(request, "faculty/changepassword.html", {'error': error})
    else:
        error = "Please enter right password!!"
        return render(request, "faculty/changepassword.html", {'error': error})

def view_mark_home(request):
    return render(request, 'faculty/view_mark_home.html')

def view_mark_year_sub(request):
    year = request.POST["year"]
    semester = request.POST["semester"]
    username = request.session.get('username')
    teacher_assign = AssignTeacher.objects.filter(employee_code=username, year_of_assign=year, semester=semester)
    obj = teacher_assign.count()

    if obj == 0:
        messages.error(request, 'No courses have been allotted according to the given year and semester')
        return render(request, 'faculty/mark_entry_home.html',{} )
    else:

        return render(request, 'faculty/view_mark_selection.html', {'teacher_assigned': teacher_assign})

def view_mark(request):
    course_details = request.POST["course_details"]
    course_id = str(course_details)[:6]
    year = str(course_details)[6:15]
    semester = str(course_details)[15:]

    mark_objects=MarksEntry.objects.filter(course_id=course_id, year=year, semester=semester)
    if mark_objects.count()>0:
        students = MarksEntry.objects.filter(course_id=course_id, year=year, semester=semester)
        return render(request, 'faculty/view_mark.html',
                      {'students': students, 'course_id': course_id, 'year': year, 'semester': semester})

    else:
        error = 'Marks entry is not submitted for this course !!Please try again with different course'
        return render(request, "faculty/view_mark_home.html", {'error': error})


def view_mark_entry(request):
    year=request.POST['year']
    semester=request.POST['semester']
    course_id=request.POST['course_id']
    faculty=AssignTeacher.objects.get(year_of_assign=year,semester=semester,course_id=course_id)
    employee_code=faculty.employee_code
    teacher=AddFaculty.objects.get(employee_code=employee_code)
    teacher_name= teacher.first_name + " "+ teacher.last_name
    course=AddCourse.objects.get(course_id=course_id)
    course_name=course.course_name 
    single_student_mark=dict()
    view_entered=[]
    profile_details =dict()
    view_entry=dict()
    profile_details['teacher_name']=teacher_name
    profile_details['course_id']=course_id

    profile_details['employee_code']= employee_code
    profile_details['course_name']=course_name
    if semester=="Odd Semester":
        profile_details['month']="May"
    else:
        profile_details['month']="December"
    profile_details['year']=str(year)[:4]
    
    

    student_marks=MarksEntry.objects.filter(course_id=course_id,year=year,semester=semester)
    for student_mark in student_marks:
        single_student_mark['regno']=student_mark.registration_no
        name=StudentProfile.objects.get(registration_no=student_mark.registration_no)

        single_student_mark['name']= str(name.first_name) + " " + str(name.last_name)
        single_student_mark['midsem']=int(student_mark.mid_sem)
        single_student_mark['endsem']=int(student_mark.end_sem)
        single_student_mark['totalmarks']=round(int(student_mark.mid_sem)+(0.5*int(student_mark.end_sem)))
        single_student_mark['grade']=student_mark.Grade
        if student_mark.Accepted=="0":
            single_student_mark['approve']="No"
        else:
            single_student_mark['approve']="Yes"
        view_entered.append(single_student_mark.copy())
    view_entry['students']=view_entered       
    return render(request,'faculty/view_mark_entry.html',{'profile_details':profile_details,'view_entry':view_entry})

def update_details(request):
    username=request.session.get('username')
    personal_details=AddFaculty.objects.get(employee_code=username)
    print(personal_details.dob)
    dob=personal_details.dob.strftime("%Y-%m-%d")
    return render(request,'faculty/update_details.html',{'personal_details':personal_details,'dob':dob})

def update_details_sub(request):

    first_name=request.POST['first_name']
    last_name=request.POST['last_name']
    email=request.POST['emailid']
    dob= request.POST['dateofbirth']
    print(dob)
    username=request.session.get('username')
    count=0
    faculty = AddFaculty.objects.get(employee_code=username)
    print(faculty.dob)
    if  first_name.title() != faculty.first_name.title() or last_name.title() != faculty.last_name.title() or email != faculty.email or dob != str(faculty.dob):
        if email != faculty.email:
            if AddFaculty.objects.filter(email=email).exists():
                error= "Email id is already taken please try again with different email id!!"
                username = request.session.get('username')
                personal_details = AddFaculty.objects.get(employee_code=username)

                dob = personal_details.dob.strftime("%Y-%m-%d")
                return render(request, 'faculty/update_details.html',
                              {'personal_details': personal_details, 'dob': dob, 'error': error})

            else:
                AddFaculty.objects.filter(employee_code=username).update(email=email)
                count=count+1


        if first_name.title() != faculty.first_name.title():
            AddFaculty.objects.filter(employee_code=username).update(first_name=first_name)

        if last_name.title() != faculty.last_name.title():
            AddFaculty.objects.filter(employee_code=username).update(last_name=last_name)
        if dob != str(faculty.dob):
            AddFaculty.objects.filter(employee_code=username).update(dob=dob)


        success="Your provided details is updated!"
        username = request.session.get('username')
        personal_details = AddFaculty.objects.get(employee_code=username)
        print(personal_details.dob)
        dob = personal_details.dob.strftime("%Y-%m-%d")
        return render(request,'faculty/update_details.html',{'personal_details': personal_details, 'dob': dob,'success':success})

    else:
        username = request.session.get('username')
        personal_details = AddFaculty.objects.get(employee_code=username)
        print(personal_details.dob)
        dob = personal_details.dob.strftime("%Y-%m-%d")
        error = "No details are updated!!"
        return render(request, 'faculty/update_details.html', {'personal_details': personal_details, 'dob': dob,'error':error})

