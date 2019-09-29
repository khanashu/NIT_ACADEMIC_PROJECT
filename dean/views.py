from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .models import AddFaculty, AddCourse, AssignTeacher,DeanNotifications,LastDate,DeanUser
from django.contrib import messages
from faculty.models import MarksEntry, FacultyNotifications
from student.models import StudentProfile
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from itertools import groupby


def index(request):
    date=datetime.now().date().strftime("%d-%m-%Y")
    print(date)
    return render(request,'dean/adminhome.html')


def dean_evaluative_check(request):

     year =request.POST["year"]
     semester =request.POST["semester"]
     dean_check = DeanNotifications.objects.filter(year=year,semester=semester)
     if dean_check.count()==0:
         messages.error(request,"No Evaluation is submitted !Please try again later")
         return redirect('deanhome')
     else:
        notifications=DeanNotifications.objects.filter(year=year,semester=semester)
        return render(request,'dean/admin_check.html',{'notifications':notifications})


def addfaculty(request):
    return render(request, 'dean/addfaculty.html')

def addcourse(request):
    return render(request, 'dean/addcourses.html')
def assign(request):
    all_courses = AddCourse.objects.all()
    print(all_courses)

    all_teachers = AddFaculty.objects.all()
    print(all_teachers)
    return render(request, 'dean/assignteachers.html', {'courses': all_courses , 'teachers': all_teachers})

def assign_teacher_form_submission(request):
    course_id = request.POST["course_id"]
    employee_code = request.POST["employee_code"]
    year_of_assign = request.POST["year_of_assign"]
    semester = request.POST["semester"]
    added_course= AddCourse.objects.get(course_id=course_id)
    assign_teacher= AddFaculty.objects.get(employee_code=employee_code)
    try:
        teacher_assigned=AssignTeacher.objects.get(course_id=course_id,year_of_assign=year_of_assign,semester=semester)
        error="Faculty is already assigned to this course in given  year of assign and semester"
        all_courses = AddCourse.objects.all()


        all_teachers = AddFaculty.objects.all()

        return render(request, 'dean/assignteachers.html', {'courses': all_courses , 'teachers': all_teachers,'error':error})

    except ObjectDoesNotExist:

        assign_teachers = AssignTeacher(course_id=added_course, employee_code=assign_teacher,year_of_assign=year_of_assign,semester=semester )
        assign_teachers.save()
        messages.success(request, 'Faculty is assigned Successfully!')
        return redirect('assign')

def add_faculty_form_submission(request):

    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    employee_code = request.POST["employee_code"]
    password = request.POST["password"]
    re_password = request.POST["re_password"]
    dob = request.POST["dob"]
    department = request.POST["department"]
    gender = request.POST["gender"]
    try:
        teacher_code=AddFaculty.objects.get(employee_code=employee_code)
        messages.error(request,'Faculty profile with same Employee Code is already created!Please try again with different code')
        return redirect('addfaculty')
    except ObjectDoesNotExist:
        if password == re_password:
            try:
                teacher_email=AddFaculty.objects.get(email=email)
                messages.error(request,'Faculty profile with same Email is already created!Please try again with Email')
                return redirect('addfaculty')
            except ObjectDoesNotExist:
                add_faculty = AddFaculty(first_name=first_name.title(),last_name=last_name.title(), email=email, employee_code= employee_code , password=password, dob=dob, department=department, gender=gender)

                add_faculty.save()
                messages.success(request, 'Faculty is added Successfully!')
                return redirect('addfaculty')
        else:
            messages.error(request,'Password do not match!')
            return redirect('addfaculty')


def add_course_form_submission(request):

    course_id = request.POST['course_id']
    course_name = request.POST['course_name']
    print(course_name)
    credit = request.POST['credits']
    department = request.POST['department']
    course=AddCourse.objects.all()
    if len(course_id)==6:


        if course.filter(course_id__iexact=course_id).exists():
            messages.error(request,'Course ID is already added!Please try again with different Course_id')
            return redirect('addcourse')
        elif course.filter(course_name__iexact=course_name).exists():
            messages.error(request,'Course name is already added!Please try again with different Course_id')
            return redirect('addcourse')

        else:
            print('hi')
            add_course = AddCourse(course_id=course_id.upper(), course_name=course_name.title(), credits=credit, department=department)
            add_course.save()
            success="Course is added Successfully!"
            return render(request,'dean/addcourses.html',{'success':success})
    else:
        messages.error(request,'Course id must be of 6 characters!')
        return redirect('addcourse')


def evaluation_home(request):
    return render(request,'dean/evaluation_home.html')

def evaluation_year_sub(request):
    year = request.POST["year"]
    semester = request.POST["semester"]

    notifications = DeanNotifications.objects.filter(year=year, semester=semester)

    obj = notifications.count()

    if obj == 0:
        messages.error(request, 'No mark entry is submitted according to the given year and semester')
        return render(request, 'dean/evaluation_home.html', {})
    else:

        return render(request, 'dean/evaluation_selection.html', {'notifications': notifications})

def evaluation(request):
    course_info = request.POST["course_info"]
    course_id = str(course_info)[:6]
    year = str(course_info)[6:15]
    semester = str(course_info)[15:]
    print(course_id)
    print(year)
    print(semester)
    students=MarksEntry.objects.filter(course_id=course_id, year=year, semester=semester , Accepted=0)
    return render(request, 'dean/evaluation.html',
                          {'students': students, 'course_id': course_id, 'year': year, 'semester': semester})

def dean_verdict(request):
    year = request.POST["year"]
    semester = request.POST["semester"]
    course_id = request.POST["course_id"]
    if 'accept' in request.POST:
        teacher=AssignTeacher.objects.get(year_of_assign=year,semester=semester,course_id=course_id)
        employee_code=teacher.employee_code.employee_code
        faculty=AddFaculty.objects.get(employee_code=employee_code)

        notifications=FacultyNotifications.objects.create(employee_code=faculty,year=year,semester=semester,course_id=course_id,accepted=1)
        notifications.save()
        DeanNotifications.objects.filter(year=year, semester=semester, course_id=course_id).delete()

        MarksEntry.objects.filter(year=year,semester=semester,course_id=course_id).update(Accepted='1')
        success="you have successfully accepted the submitted mark entry!"

        return render(request,"dean/evaluation_home.html",{'success':success})
    else:
        DeanNotifications.objects.filter(year=year, semester=semester, course_id=course_id).delete()
        MarksEntry.objects.filter(year=year, semester=semester, course_id=course_id).delete()
        teacher = AssignTeacher.objects.get(year_of_assign=year, semester=semester, course_id=course_id)
        employee_code = teacher.employee_code.employee_code
        faculty=AddFaculty.objects.get(employee_code=employee_code)
        notifications = FacultyNotifications.objects.create(employee_code=faculty, year=year, semester=semester,
                                                            course_id=course_id)
        notifications.save()
        error="you have successfully declined the submitted mark entry"
        return render(request,"dean/evaluation_home.html",{'error':error})
def grade_card_generate(request):
    students=StudentProfile.objects.all()
    return render(request,"dean/grade_card_generation.html",{'students':students})
def grade_card(request):
    profile_details =dict()
    grades_entry = dict()
    single_subject_grade_entry=dict()
    grade_entered=[]
    credits_reg=dict()
    credits_earned=dict()
    credits_earned['one']=0
    credits_earned['two']=0
    credits_earned['three']=0
    credits_earned['four']=0
    credits_earned['five']=0
    credits_earned['six']=0
    credits_earned['seven']=0
    credits_earned['eight']=0
    credits_earned['nine']=0
    credits_earned['ten']=0
    credits_reg['one'] =0
    credits_reg['two'] = 0
    credits_reg['three'] =0
    credits_reg['four'] =0
    credits_reg['five'] =0
    credits_reg['six'] = 0
    credits_reg['seven'] = 0
    credits_reg['eight'] = 0
    credits_reg['nine'] = 0
    credits_reg['ten'] =0
    credits_reg['none']='#'
    credits_reg['total']=0
    credits_reg['total_grades']=0
    registration_no=request.POST['registration_no']
    student_profile=StudentProfile.objects.get(registration_no=registration_no)
    profile_details['first_name']=student_profile.first_name
    profile_details['last_name']=student_profile.last_name

    profile_details['regno']= student_profile.registration_no
    profile_details['gender']=student_profile.gender
    profile_details['branch']=student_profile.branch
    profile_details['date_publish']=datetime.now().date().strftime("%d-%b-%Y")
    profile_details['dob']=student_profile.dateofbirth.strftime("%d-%b-%Y")



    student_marks=MarksEntry.objects.filter(registration_no=registration_no)
    if student_marks.count()>=2:
        for student_mark in student_marks:

            month_of_reg=student_profile.monthofreg
            year_of_reg=int(student_profile.yearofreg)
            first_month="January"

            second_month="July"
            if month_of_reg.title()==first_month:
                odd_sem="Odd Semester"
                even_sem="Even Semester"
                sem=student_mark.semester
                count=0
                year=student_mark.year
                check=int(str(year)[0:4])
                month=""

                while year_of_reg < check:
                    count=count+2
                    year_of_reg+=1




                if sem==odd_sem:
                    month="MAY"
                    count=count+1

                else:
                    count=count+2
                    month="DEC"

                single_subject_grade_entry['semester']=count
                single_subject_grade_entry['course_id']=student_mark.course_id
                course_id= student_mark.course_id
                course=AddCourse.objects.get(course_id=course_id)
                single_subject_grade_entry['course_name']=course.course_name
                if student_mark.Grade=='U' or student_mark.Grade=='AB':
                    single_subject_grade_entry['credits']=0
                else:
                    single_subject_grade_entry['credits'] = course.credits

                single_subject_grade_entry['grade']=student_mark.Grade
                single_subject_grade_entry['gradepoint']=grade_calc(student_mark.Grade)
                single_subject_grade_entry['month']=month
                single_subject_grade_entry['year']=year_of_reg
                credits_reg['total_grades']= credits_reg['total_grades'] + float(grade_calc(student_mark.Grade))*float(course.credits)
                if count == 1:
                    credits_reg['one']=int(credits_reg['one']) +int(course.credits)
                if count == 2:
                    credits_reg['two'] =int(credits_reg['two'])+ int(course.credits)
                if count == 3:
                    credits_reg['three'] = int(credits_reg['three']) + int(course.credits)
                if count == 4:
                    credits_reg['four'] =  int(credits_reg['four']) +int(course.credits)
                if count == 5:
                    credits_reg['five'] =  int(credits_reg['five']) + int(course.credits)
                if count == 6:
                    credits_reg['six'] =  int(credits_reg['six']) + int(course.credits)
                if count == 7:
                    credits_reg['seven'] = int(credits_reg['seven']) +  int(course.credits)
                if count == 8:
                    credits_reg['eight'] = int(credits_reg['eight'])+ int(course.credits)
                if count == 9:
                    credits_reg['nine'] = int(credits_reg['nine'])+int(course.credits)
                if count == 10:
                    credits_reg['ten'] = int(credits_reg['ten'])+ int(course.credits)

                if count == 1:
                    credits_earned['one']=int(credits_earned['one']) +int(single_subject_grade_entry['credits'])
                if count == 2:
                    credits_earned['two'] =int(credits_earned['two'])+ int(single_subject_grade_entry['credits'])
                if count == 3:
                    credits_earned['three'] = int(credits_earned['three']) + int(single_subject_grade_entry['credits'])
                if count == 4:
                    credits_earned['four'] =  int(credits_earned['four']) + int(single_subject_grade_entry['credits'])
                if count == 5:
                    credits_earned['five'] =  int(credits_earned['five']) + int(single_subject_grade_entry['credits'])
                if count == 6:
                    credits_earned['six'] =  int(credits_earned['six']) + int(single_subject_grade_entry['credits'])
                if count == 7:
                    credits_earned['seven'] = int(credits_earned['seven']) + int(single_subject_grade_entry['credits'])
                if count == 8:
                    credits_earned['eight'] = int(credits_earned['eight'])+ int(single_subject_grade_entry['credits'])
                if count == 9:
                    credits_earned['nine'] = int(credits_earned['nine'])+ int(single_subject_grade_entry['credits'])
                if count == 10:
                    credits_earned['ten'] = int(credits_earned['ten'])+ int(single_subject_grade_entry['credits'])
                single_subject_grade_entry['credits'] = course.credits
                grade_entered.append(single_subject_grade_entry.copy())



            else:

                odd_sem = "Odd Semester"
                even_sem = "Even Semester"
                sem = student_mark.semester

                year = student_mark.year
                check = int(str(year)[0:4])
                month=""
                if year_of_reg == check:
                    count =1
                    month ="DEC"
                else:
                    count=1
                    if year_of_reg==(check-1):

                        if sem == odd_sem:
                            month = "MAY"
                            count = count + 1
                        else:
                            month = "DEC"
                            count = count + 2
                        year_of_reg=year_of_reg + 1
                    else:
                        while year_of_reg < check:
                            count=count+2
                            year_of_reg=year_of_reg+1

                        if sem==odd_sem:
                            month="DEC"
                            count=count+2
                        else:
                            month="MAY"
                            count=count+1
                single_subject_grade_entry['semester'] = count
                single_subject_grade_entry['course_id'] = student_mark.course_id
                course_id = student_mark.course_id
                course = AddCourse.objects.get(course_id=course_id)
                single_subject_grade_entry['course_name'] = course.course_name
                if student_mark.Grade=='U' or student_mark.Grade=='AB':
                    single_subject_grade_entry['credits']=0
                else:
                    single_subject_grade_entry['credits'] = course.credits
                single_subject_grade_entry['grade'] = student_mark.Grade
                single_subject_grade_entry['gradepoint'] = grade_calc(student_mark.Grade)
                single_subject_grade_entry['month'] = month
                single_subject_grade_entry['year'] = year_of_reg
                credits_reg['total_grades'] = credits_reg['total_grades'] + float(grade_calc(student_mark.Grade)) * float(course.credits)

                if count == 1:
                    credits_reg['one']=int(credits_reg['one']) +int(course.credits)
                if count == 2:
                    credits_reg['two'] =int(credits_reg['two'])+ int(course.credits)
                if count == 3:
                    credits_reg['three'] = int(credits_reg['three']) + int(course.credits)
                if count == 4:
                    credits_reg['four'] =  int(credits_reg['four']) +int(course.credits)
                if count == 5:
                    credits_reg['five'] =  int(credits_reg['five']) + int(course.credits)
                if count == 6:
                    credits_reg['six'] =  int(credits_reg['six']) + int(course.credits)
                if count == 7:
                    credits_reg['seven'] = int(credits_reg['seven']) +  int(course.credits)
                if count == 8:
                    credits_reg['eight'] = int(credits_reg['eight'])+ int(course.credits)
                if count == 9:
                    credits_reg['nine'] = int(credits_reg['nine'])+int(course.credits)
                if count == 10:
                    credits_reg['ten'] = int(credits_reg['ten'])+ int(course.credits)

                if count == 1:
                    credits_earned['one']=int(credits_earned['one']) +int(single_subject_grade_entry['credits'])
                if count == 2:
                    credits_earned['two'] =int(credits_earned['two'])+ int(single_subject_grade_entry['credits'])
                if count == 3:
                    credits_earned['three'] = int(credits_earned['three']) + int(single_subject_grade_entry['credits'])
                if count == 4:
                    credits_earned['four'] =  int(credits_earned['four']) + int(single_subject_grade_entry['credits'])
                if count == 5:
                    credits_earned['five'] =  int(credits_earned['five']) + int(single_subject_grade_entry['credits'])
                if count == 6:
                    credits_earned['six'] =  int(credits_earned['six']) + int(single_subject_grade_entry['credits'])
                if count == 7:
                    credits_earned['seven'] = int(credits_earned['seven']) + int(single_subject_grade_entry['credits'])
                if count == 8:
                    credits_earned['eight'] = int(credits_earned['eight'])+ int(single_subject_grade_entry['credits'])
                if count == 9:
                    credits_earned['nine'] = int(credits_earned['nine'])+ int(single_subject_grade_entry['credits'])
                if count == 10:
                    credits_earned['ten'] = int(credits_earned['ten'])+ int(single_subject_grade_entry['credits'])
                single_subject_grade_entry['credits'] = course.credits
                grade_entered.append(single_subject_grade_entry.copy())


            grades_entry['students']=grade_entered
            credits_reg['total'] =credits_reg['one']+credits_reg['two'] + credits_reg['three'] + credits_reg['four'] + credits_reg['five'] + credits_reg['six'] + credits_reg['seven'] + credits_reg['eight'] + credits_reg['nine'] +credits_reg['ten']
            print(credits_reg['total'])
            credits_earned['total'] =credits_earned['one']+credits_earned['two'] + credits_earned['three'] + credits_earned['four'] + credits_earned['five'] + credits_earned['six'] + credits_earned['seven'] + credits_earned['eight'] + credits_earned['nine'] +credits_earned['ten']
            x=float(credits_reg['total_grades'])/float(credits_reg['total'])
            credits_reg['cgpa']= format(x,'.2f')
            serial_no= str(registration_no)[2:4]+"00"+str(registration_no)[6:10]


        return render(request,'student/gradecard.html',{'profile_details':profile_details,'grades_entry':grades_entry,'credits_reg':credits_reg,'serial_no':serial_no,'credits_earned':credits_earned})
    else:
        error="Grade card cannot be generated because the number of courses completed by student is not 4!!"
        students = StudentProfile.objects.all()
        return render(request,"dean/grade_card_generation.html",{'error':error,'students':students})

def grade_calc(grade):
    grade=str(grade)
    if grade == 'S':
        point=10
    if grade == 'A':
        point=9
    if grade == 'B':
        point=8
    if grade == 'C':
        point=7
    if grade == 'D':
        point=6
    if grade == 'E':
        point=5
    if grade == 'U':
        point=0
    if grade == 'I':
        point=0
    if grade == 'AB':
        point =0


    return point

def last_date_mark(request):
    return render(request,"dean/last_date_mark.html")

def last_date_mark_submission(request):
    year=request.POST["year"]
    semester=request.POST["semester"]
    date=request.POST["date"]
    if AssignTeacher.objects.filter(year_of_assign=year,semester=semester).exists():
        if MarksEntry.objects.filter(year=year,semester=semester,Accepted=0).exists():
            if LastDate.objects.get(year=year,semester=semester).exists():
                error="Date cannot be assigned as the last date of mark entry is already assigned for given year ann semester "
                return render(request,"dean/last_date_mark.html",{'error':error})
            else:
                lastdate=LastDate.objects.create(year=year,semester=semester,date=date)
                lastdate.save()
                success="Last Date notification is submitted for teachers"
                return render(request,"dean/last_date_mark.html",{'success':success})
        else:
            if MarksEntry.objects.filter(year=year, semester=semester, Accepted=1).exists():
                error="Last date cannot be submitted as all the teachers have already submitted their mark entry with verification from dean"
                return render(request,"dean/last_date_mark.html",{'error':error})
            else:
               try:
                    LastDate.objects.filter(year=year, semester=semester).exists()
                    error = "Date cannot be assigned as the last date of mark entry is already assigned for given year ann semester "
                    return render(request, "dean/last_date_mark.html", {'error': error})

               except ObjectDoesNotExist:
                    lastdate = LastDate.objects.create(year=year, semester=semester, date=date)
                    lastdate.save()
                    success = "Last Date notification is submitted for teachers"
                    return render(request, "dean/last_date_mark.html", {'success': success})


    else:
        error="Date cannot be submitted as no teacher is assigned any course according to given year and semester "
        return render(request, "dean/last_date_mark.html", {'error': error})

def changepassword(request):
    return render(request,"dean/changepassword.html")

def changepasswordsubmission(request):
    oldpassword=request.POST["oldpassword"]
    newpassword=request.POST["newpassword"]
    renewpassword=request.POST["renewpassword"]
    username=request.session.get('username')
    dean_instance=DeanUser.objects.get(username=username)
    if dean_instance.password==oldpassword:
        if newpassword==renewpassword:
            DeanUser.objects.filter(username=username,password=oldpassword).update(password=newpassword)
            success="Password changed successfully!"
            return render(request,"dean/changepassword.html",{'success':success})
        else:
            error="New Password field do not match with Retype New Password field!"
            return render(request,"dean/changepassword.html",{'error':error})
    else:
        error = "Please enter right password!!"
        return render(request, "dean/changepassword.html", {'error': error})
def dean_logout(request):
    request.session.clear()
    return redirect('login')


def report_home(request):
    return render(request,"dean/report_home.html")

def report_sub( request,*args,**kwargs):
    template= get_template('dean/report.html')
    occurence_list=[]
    iterate=[]
    year =request.POST["year"]
    branch=request.POST["department"]
    semester=request.POST["semester"]
    yearofreg =str(year)[0:4]
    print(semester)
    name_of_students=StudentProfile.objects.filter(yearofreg=yearofreg,branch=branch)
    for student in name_of_students:
        student_occured=MarksEntry.objects.filter(registration_no=student.registration_no,semester=semester)
        for student_list in student_occured:
            occurence_list.append(student_list.registration_no)

    occurrence, num_times = 0, 0
    for key, values in groupby(occurence_list, lambda x: x):
        val = len(list(values))
        if val >= occurrence:
            occurrence, num_times = key, val


    num = int(num_times)
    each_student_details=dict()
    final_merge_list=[]
    for student in name_of_students:

        registration_no = student.registration_no
        print(registration_no)
        profile_details =dict()
        grades_entry = dict()
        single_subject_grade_entry=dict()
        grade_entered=[]
        credits_reg=dict()
        credits_earned=dict()
        credits_earned['one']=0
        credits_earned['two']=0
        credits_earned['three']=0
        credits_earned['four']=0
        credits_earned['five']=0
        credits_earned['six']=0
        credits_earned['seven']=0
        credits_earned['eight']=0
        credits_earned['nine']=0
        credits_earned['ten']=0
        credits_reg['one_reg'] =0
        credits_reg['two_reg'] = 0
        credits_reg['three_reg'] =0
        credits_reg['four_reg'] =0
        credits_reg['five_reg'] =0
        credits_reg['six_reg'] = 0
        credits_reg['seven_reg'] = 0
        credits_reg['eight_reg'] = 0
        credits_reg['nine_reg'] = 0
        credits_reg['ten_reg'] =0
        credits_reg['none_reg']='#'
        credits_reg['total_reg']=0
        credits_reg['total_grades_reg']=0

        student_profile=StudentProfile.objects.get(registration_no=registration_no)
        profile_details['first_name']=student_profile.first_name
        profile_details['last_name']=student_profile.last_name

        profile_details['regno']= student_profile.registration_no
        profile_details['gender']=student_profile.gender
        profile_details['branch']=student_profile.branch
        profile_details['date_publish']=datetime.now().date().strftime("%d-%b-%Y")
        profile_details['dob']=student_profile.dateofbirth.strftime("%d/%m/%Y")
        serial_no= str(registration_no)[2:4]+"00"+str(registration_no)[6:10]
        profile_details['serialno']=serial_no

        student_marks=MarksEntry.objects.filter(registration_no=registration_no)
        if student_marks.count()>=0:
            for student_mark in student_marks:

                month_of_reg=student_profile.monthofreg
                year_of_reg=int(student_profile.yearofreg)
                first_month="January"

                second_month="July"
                if month_of_reg.title()==first_month:
                    odd_sem="Odd Semester"
                    even_sem="Even Semester"
                    sem=student_mark.semester
                    count=0
                    year=student_mark.year
                    check=int(str(year)[0:4])
                    month=""

                    while year_of_reg < check:
                        count=count+2
                        year_of_reg+=1




                    if sem==odd_sem:
                        month="MAY"
                        count=count+1

                    else:
                        count=count+2
                        month="DEC"

                    single_subject_grade_entry['semester']=count
                    single_subject_grade_entry['course_id']=student_mark.course_id
                    course_id= student_mark.course_id
                    course=AddCourse.objects.get(course_id=course_id)
                    single_subject_grade_entry['course_name']=course.course_name
                    if student_mark.Grade=='U' or student_mark.Grade=='AB':
                        single_subject_grade_entry['credits']=0
                    else:
                        single_subject_grade_entry['credits'] = course.credits

                    single_subject_grade_entry['grade']=student_mark.Grade
                    single_subject_grade_entry['gradepoint']=grade_calc(student_mark.Grade)
                    single_subject_grade_entry['month']=month
                    single_subject_grade_entry['year']=year_of_reg
                    credits_reg['total_grades_reg']= credits_reg['total_grades_reg'] + float(grade_calc(student_mark.Grade))*float(course.credits)
                    if count == 1:
                        credits_reg['one_reg']=int(credits_reg['one_reg']) +int(course.credits)
                    if count == 2:
                        credits_reg['two_reg'] =int(credits_reg['two_reg'])+ int(course.credits)
                    if count == 3:
                        credits_reg['three_reg'] = int(credits_reg['three_reg']) + int(course.credits)
                    if count == 4:
                        credits_reg['four_reg'] =  int(credits_reg['four_reg']) +int(course.credits)
                    if count == 5:
                        credits_reg['five_reg'] =  int(credits_reg['five_reg']) + int(course.credits)
                    if count == 6:
                        credits_reg['six_reg'] =  int(credits_reg['six_reg']) + int(course.credits)
                    if count == 7:
                        credits_reg['seven_reg'] = int(credits_reg['seven_reg']) +  int(course.credits)
                    if count == 8:
                        credits_reg['eight_reg'] = int(credits_reg['eight_reg'])+ int(course.credits)
                    if count == 9:
                        credits_reg['nine_reg'] = int(credits_reg['nine_reg'])+int(course.credits)
                    if count == 10:
                        credits_reg['ten_reg'] = int(credits_reg['ten_reg'])+ int(course.credits)

                    if count == 1:
                        credits_earned['one']=int(credits_earned['one']) +int(single_subject_grade_entry['credits'])
                    if count == 2:
                        credits_earned['two'] =int(credits_earned['two'])+ int(single_subject_grade_entry['credits'])
                    if count == 3:
                        credits_earned['three'] = int(credits_earned['three']) + int(single_subject_grade_entry['credits'])
                    if count == 4:
                        credits_earned['four'] =  int(credits_earned['four']) + int(single_subject_grade_entry['credits'])
                    if count == 5:
                        credits_earned['five'] =  int(credits_earned['five']) + int(single_subject_grade_entry['credits'])
                    if count == 6:
                        credits_earned['six'] =  int(credits_earned['six']) + int(single_subject_grade_entry['credits'])
                    if count == 7:
                        credits_earned['seven'] = int(credits_earned['seven']) + int(single_subject_grade_entry['credits'])
                    if count == 8:
                        credits_earned['eight'] = int(credits_earned['eight'])+ int(single_subject_grade_entry['credits'])
                    if count == 9:
                        credits_earned['nine'] = int(credits_earned['nine'])+ int(single_subject_grade_entry['credits'])
                    if count == 10:
                        credits_earned['ten'] = int(credits_earned['ten'])+ int(single_subject_grade_entry['credits'])
                    single_subject_grade_entry['credits'] = course.credits
                    grade_entered.append(single_subject_grade_entry.copy())



                else:

                    odd_sem = "Odd Semester"
                    even_sem = "Even Semester"
                    sem = student_mark.semester

                    year = student_mark.year
                    check = int(str(year)[0:4])
                    month=""
                    if year_of_reg == check:
                        count =1
                        month ="DEC"
                    else:
                        count=1
                        if year_of_reg==(check-1):

                            if sem == odd_sem:
                                month = "MAY"
                                count = count + 1
                            else:
                                month = "DEC"
                                count = count + 2
                            year_of_reg=year_of_reg + 1
                        else:
                            while year_of_reg < check:
                                count=count+2
                                year_of_reg=year_of_reg+1

                            if sem==odd_sem:
                                month="DEC"
                                count=count+2
                            else:
                                month="MAY"
                                count=count+1
                    single_subject_grade_entry['semester'] = count
                    single_subject_grade_entry['course_id'] = student_mark.course_id
                    course_id = student_mark.course_id
                    course = AddCourse.objects.get(course_id=course_id)
                    single_subject_grade_entry['course_name'] = course.course_name
                    if student_mark.Grade=='U' or student_mark.Grade=='AB':
                        single_subject_grade_entry['credits']=0
                    else:
                        single_subject_grade_entry['credits'] = course.credits
                    single_subject_grade_entry['grade'] = student_mark.Grade
                    single_subject_grade_entry['gradepoint'] = grade_calc(student_mark.Grade)
                    single_subject_grade_entry['month'] = month
                    single_subject_grade_entry['year'] = year_of_reg
                    credits_reg['total_grades_reg'] = credits_reg['total_grades_reg'] + float(grade_calc(student_mark.Grade)) * float(course.credits)

                    if count == 1:
                        credits_reg['one_reg']=int(credits_reg['one_reg']) +int(course.credits)
                    if count == 2:
                        credits_reg['two_reg'] =int(credits_reg['two_reg'])+ int(course.credits)
                    if count == 3:
                        credits_reg['three_reg'] = int(credits_reg['three_reg']) + int(course.credits)
                    if count == 4:
                        credits_reg['four_reg'] =  int(credits_reg['four_reg']) +int(course.credits)
                    if count == 5:
                        credits_reg['five_reg'] =  int(credits_reg['five_reg']) + int(course.credits)
                    if count == 6:
                        credits_reg['six_reg'] =  int(credits_reg['six_reg']) + int(course.credits)
                    if count == 7:
                        credits_reg['seven_reg'] = int(credits_reg['seven_reg']) +  int(course.credits)
                    if count == 8:
                        credits_reg['eight_reg'] = int(credits_reg['eight_reg'])+ int(course.credits)
                    if count == 9:
                        credits_reg['nine_reg'] = int(credits_reg['nine_reg'])+int(course.credits)
                    if count == 10:
                        credits_reg['ten_reg'] = int(credits_reg['ten_reg'])+ int(course.credits)

                    if count == 1:
                        credits_earned['one']=int(credits_earned['one']) +int(single_subject_grade_entry['credits'])
                    if count == 2:
                        credits_earned['two'] =int(credits_earned['two'])+ int(single_subject_grade_entry['credits'])
                    if count == 3:
                        credits_earned['three'] = int(credits_earned['three']) + int(single_subject_grade_entry['credits'])
                    if count == 4:
                        credits_earned['four'] =  int(credits_earned['four']) + int(single_subject_grade_entry['credits'])
                    if count == 5:
                        credits_earned['five'] =  int(credits_earned['five']) + int(single_subject_grade_entry['credits'])
                    if count == 6:
                        credits_earned['six'] =  int(credits_earned['six']) + int(single_subject_grade_entry['credits'])
                    if count == 7:
                        credits_earned['seven'] = int(credits_earned['seven']) + int(single_subject_grade_entry['credits'])
                    if count == 8:
                        credits_earned['eight'] = int(credits_earned['eight'])+ int(single_subject_grade_entry['credits'])
                    if count == 9:
                        credits_earned['nine'] = int(credits_earned['nine'])+ int(single_subject_grade_entry['credits'])
                    if count == 10:
                        credits_earned['ten'] = int(credits_earned['ten'])+ int(single_subject_grade_entry['credits'])
                    single_subject_grade_entry['credits'] = course.credits
                    grade_entered.append(single_subject_grade_entry.copy())



                credits_reg['total_reg'] =credits_reg['one_reg']+credits_reg['two_reg'] + credits_reg['three_reg'] + credits_reg['four_reg'] + credits_reg['five_reg'] + credits_reg['six_reg'] + credits_reg['seven_reg'] + credits_reg['eight_reg'] + credits_reg['nine_reg'] +credits_reg['ten_reg']

                credits_earned['total'] =credits_earned['one']+credits_earned['two'] + credits_earned['three'] + credits_earned['four'] + credits_earned['five'] + credits_earned['six'] + credits_earned['seven'] + credits_earned['eight'] + credits_earned['nine'] +credits_earned['ten']
                x=float(credits_reg['total_grades_reg'])/float(credits_reg['total_reg'])
                credits_reg['cgpa']= format(x,'.2f')
        profile_details['grades']=grade_entered
        profile_details.update(credits_reg.copy())
        profile_details.update(credits_earned.copy())
        final_merge_list.append(profile_details.copy())

    each_student_details['students']=final_merge_list
    context={
        'range':range(num),'each_student_details':each_student_details,'branch':branch,'yearofreg':yearofreg
    }
    html=template.render(context)
    
    return HttpResponse(html)

  

