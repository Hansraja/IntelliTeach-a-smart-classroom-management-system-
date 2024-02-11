from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from Admin.models import Student

class HomePage:
    def as_view(request):
        if request.user.is_authenticated:
            if request.user.is_faculty:
                return redirect('/faculty_dashboard')
            else:
                return redirect('/student_dashboard')
            
        title = 'Home'
        if request.method == 'POST': # type: ignore
            password = request.POST['password'] # type: ignore
            selected = request.POST.get('selected', False)  # type: ignore
            if selected == 'faculty':
                email = request.POST['email'] # type: ignore
                user = authenticate(request, username=email, password=password)
                if user is not None and user.is_faculty: # type: ignore
                    login(request, user) # type: ignore
                    return redirect('/faculty_dashboard')
                else:
                    return render(request=request, template_name='index.html', context={'title':title, 'messages': [{'text': 'Invalid Email or Password', 'type': 'error'}], 'selected': 'faculty'}) # type: ignore
            elif selected == 'student':
                roll_number = request.POST.get('roll_number', False) # type: ignore
                print(roll_number, type(roll_number))
                try:
                    student = Student.objects.get(roll_number= roll_number)
                    if student and student.email: # type: ignore
                        user = authenticate(request, username=student.email, password=password) # type: ignore
                        if user is not None and user.is_student: # type: ignore
                            login(request, user) # type: ignore
                            return redirect('/')   
                        else:
                            messages = [{'text': 'Invalid Roll Number or Password', 'type': 'error'}]
                            return render(request=request, template_name='index.html', context={'title':title, 'messages': messages, 'selected': selected}) # type: ignore    
                    else: 
                        messages = [{'text': 'Invalid Roll Number or Password', 'type': 'error'}]
                        return render(request=request, template_name='index.html', context={'title':title, 'messages': messages, 'selected': selected}) # type: ignore
                except:
                    messages = [{'text': 'Invalid Roll Number or Password', 'type': 'error'}]
                    return render(request=request, template_name='index.html', context={'title': title, 'messages': messages, 'selected': selected}) # type: ignore
            else:
                messages = [{'text': 'Something went wrong', 'type': 'error'}]
                return render(request=request, template_name='index.html', context={'title': title, 'messages': messages, 'selected': selected}) # type: ignore
        return render(request=request, template_name='index.html', context={'title':title}) # type: ignore
    
@login_required
def facultyDashboard(request):
    if not request.user.is_faculty:
        return redirect('/')
    title = 'Faculty Dashboard'
    return render(request, 'faculty_dashboard.html', {'title': title}) # type: ignore

@login_required
def studentDashboard(request):
    if not request.user.is_student:
        return redirect('/')
    title = 'Student Dashboard'
    return render(request, 'student_dashboard.html', {'title': title})