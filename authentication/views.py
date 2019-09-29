from django.shortcuts import render, redirect
from .auth import login


def index(request):
    redirect_target = get_redirect_target(request)
    if redirect_target is not None:
        return redirect(redirect_target)
    else:
        if request.method == 'POST':
            return login(request)
        else:
            return render(request, 'authentication/login.html', {})




def get_redirect_target(request):
    if not request.session.get('logged'):
        return None
    user_type = request.session.get('user_type')
    if user_type == 'faculty':
        return 'facultyhome'

    if user_type == 'student':
        return 'studenthome'

    if user_type == 'dean':
        return 'deanhome'

    return None