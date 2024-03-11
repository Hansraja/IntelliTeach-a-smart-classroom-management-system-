from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import AuthUser
from Home.models import Student_Notice
import json
from django.conf import settings

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
        elif user is not None  and user.is_hod: # type: ignore
            login(request, user)
            return redirect('admin_dashboard')
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
    notices = Student_Notice.objects.all().order_by('-created_at')
    context = {'title': f"Admin - {settings.APP_NAME}", 'notices': notices}
    return render(request, 'admin.html', context=context)


def update_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_faculty or request.user.is_hod : # type: ignore
                    try:
                        data = request.body.decode('utf-8')
                        data = json.loads(data)
                        _id = data.get('_id', None)
                        user = AuthUser.objects.get(id=int(_id))
                        password = data.get('password', None)
                        confirm_password = data.get('confirm_password', None)
                        if password:
                            if password == confirm_password:
                                user.set_password(password)
                                user.save()
                                return JsonResponse({'success': True, 'message': 'Password updated successfully'})
                            else:
                                return JsonResponse({'success': False, 'message': 'New password and confirm password do not match'})
                        else:
                            return JsonResponse({'success': False, 'message': 'Please enter a valid password'})
                    except Exception as e:
                        print(e)
                        return JsonResponse({'success': False, 'message': 'An error occurred while updating password'})
            else:
                return JsonResponse({'success': False, 'message': 'You are not authorized to perform this action'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not logged in'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required(login_url='home')
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

@login_required(login_url='home')
def add_notice(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_hod or request.user.is_faculty: # type: ignore
            title = request.POST.get('title', None)
            description = request.POST.get('description', None)
            attachment = request.FILES.get('attachment', None)
            try:
                notice = Student_Notice.objects.create(title=title, message=description, attachment=attachment, admin=request.user)
                try:
                    notice.send_to_email()
                except Exception as e:
                    print(e)
                    return JsonResponse({'success': True, 'message': f'Notice added successfully, but an error occurred while sending email to students. \n-----> {e}'})
                return JsonResponse({'success': True, 'message': 'Notice added successfully'})
            except Exception as e:
                print(e)
                return JsonResponse({'success': False, 'message': 'An error occurred while adding notice'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not authorized to perform this action'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required(login_url='home')
def delete_notice(request, id):
    try:
        notice = Student_Notice.objects.get(id=int(id))
        notice.delete()
        return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')