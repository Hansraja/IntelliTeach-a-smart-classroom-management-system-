from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import menu
from Admin.models import AuthUser

title = 'Faculty Dashboard'

@login_required(login_url='/')
def facultyDashboard(request):
    if not request.user.is_faculty:
        return redirect('/')
    return render(request, 'faculty_dashboard.html', {'title': title, 'menuItems': menu }) # type: ignore


def faculty_Profile(request):

    context = {'title': title, 'menuItems': menu }
    return render(request, 'settings/profile.html', context=context)

def add_student(request):
    context = {'title': title, 'menuItems': menu }
    return render(request, 'faculty/add_students.html', context=context)

