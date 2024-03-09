import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from Admin.models import Student, Faculty


def home_login(request):
    if request.user.is_authenticated: # type: ignore
        if request.user.is_faculty: # type: ignore
            return redirect('teacher_dashboard')
        elif request.user.is_student:
            title = 'Student Dashboard'
            return render(request, 'student/dashboard.html', {'title': 'title'})
        else:
            return redirect('admin_dashboard')
        
    title = f'Login to {settings.APP_NAME}'
    if request.method == 'POST': # type: ignore
        password = request.POST['password'] # type: ignore
        selected = request.POST.get('selected', None)  # type: ignore
        if selected == 'faculty':
            email = request.POST['email'] # type: ignore
            user = authenticate(request, username=email, password=password)
            faculty = Faculty.objects.get(user_id=user.id) if user else None # type: ignore
            if user is not None and user.is_faculty and faculty: # type: ignore
                login(request, user) # type: ignore
                return redirect('teacher_dashboard')
            else:
                return render(request=request, template_name='index.html', context={'title':title, 'messages': [{'text': 'Invalid Email or Password', 'type': 'error'}], 'selected': 'faculty'}) # type: ignore
        elif selected == 'student':
            roll_number = request.POST.get('roll_number', None) # type: ignore
            try:
                student = Student.objects.get(roll_number=roll_number)
                if student and student.user.email: # type: ignore
                    user = authenticate(request, username=student.user.email, password=password) # type: ignore
                    if user is not None and user.is_student: # type: ignore
                        login(request, user) # type: ignore
                        return redirect('/')   
                    else:
                        messages = [{'text': 'Invalid Roll Number or Password', 'type': 'error'}]
                        return render(request=request, template_name='index.html', context={'title':title, 'messages': messages, 'selected': selected}) # type: ignore    
                else: 
                    messages = [{'text': 'Invalid Roll Number or Password', 'type': 'error'}]
                    return render(request=request, template_name='index.html', context={'title':title, 'messages': messages, 'selected': selected}) # type: ignore
            except Exception as e:
                print(e, f'Got error while logging Student {roll_number} ...')
                messages = [{'text': 'Invalid Roll Number or Password', 'type': 'error'}]
                return render(request=request, template_name='index.html', context={'title': title, 'messages': messages, 'selected': selected}) # type: ignore
        else:
            messages = [{'text': 'Something went wrong', 'type': 'error'}]
            return render(request=request, template_name='index.html', context={'title': title, 'messages': messages, 'selected': selected}) # type: ignore
    return render(request=request, template_name='index.html', context={'title':title}) # type: ignore

@login_required(login_url='/')
def studentDashboard(request):
    if not request.user.is_student:
        return redirect('/')
    title = 'Student Dashboard'
    return render(request, 'student/dashboard.html', {'title': title})


def Images(request, path: str):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/jpeg")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404