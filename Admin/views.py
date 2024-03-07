from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import AuthUser

def hod_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_hod: # type: ignore
            login(request, user)
            return redirect('hod_dashboard')  # Replace with actual HOD dashboard URL
        else:
            # Handle invalid login for HOD
            pass

    return render(request, 'index.html')

def faculty_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_faculty: # type: ignore
            login(request, user)
            return redirect('faculty_dashboard')
        else:
            pass

    return render(request, 'index.html')

def student_login(request):
    if request.method == 'POST':
        roll_number = request.POST['roll_number']
        password = request.POST['password']
        user = authenticate(request, username=roll_number, password=password)

        if user is not None and user.is_student: # type: ignore
            login(request, user)
            return redirect('student_dashboard')
        else:
            pass
    return render(request, 'index.html')


def admin_dashboard(request):
    return render(request, 'admin.html')
