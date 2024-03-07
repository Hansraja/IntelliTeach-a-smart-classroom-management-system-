from django.forms import ValidationError
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import menu
from Admin.models import AuthUser, Faculty

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

def teachers_list(request):
    data = Faculty.objects.all()
    context = {'title': title,'teachers': data}
    return render(request, 'teachers.html', context=context)


def update_teacher(request):
    if request.method == 'POST':
        _id = request.POST.get('id', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        subject = request.POST.get('subject', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        image = request.FILES.get('image', None)
        try:
            teacher = Faculty.objects.get(id=_id)
            # teacher.user.email = email if email else teacher.user.email
            teacher.user.first_name = first_name if first_name else teacher.user.first_name
            teacher.user.last_name = last_name if last_name else teacher.user.last_name
            teacher.subject = subject if subject else teacher.subject
            teacher.user.picture = image if image else teacher.user.picture # type: ignore
            teacher.mobile = mobile if mobile else teacher.mobile
            teacher.user.save()
            teacher.save()
        except ValidationError as e:
            print(e, 'got error while updating teacher')
            return HttpResponseServerError("Something went wrong, try again.")
        except Exception as e:
            print(e)
            teachers = Faculty.objects.all()
            context = {'title': 'Teacher', 'teachers': teachers, 'messages': [{'message': 'An error occurred!', 'tag': 'danger'}]}
            return render(request, 'teachers.html', context=context)
        print(teacher, 'teacher updated successfully!')
        teachers = Faculty.objects.all()
        context = {'title': 'Teacher', 'teachers': teachers, 'messages': [{'message': 'Teacher updated successfully!', 'tag': 'success'}]}
        return render(request, 'teachers.html', context=context)
    teachers = Faculty.objects.all()
    context = {'title': 'Teacher', 'teachers': teachers,}
    return render(request, 'teachers.html', context=context)

def delete_teacher(request):
    if request.method == 'POST':
        _id = request.POST.get('id', None)
        print(_id, 'teacher data', request.POST)
        try:
            teacher = Faculty.objects.get(id=_id)
            teacher.user.delete()
        except ValidationError as e:
            print(e, 'got error while deleting teacher')
            return HttpResponseServerError("Something went wrong, try again.")
        except Exception as e:
            teachers = Faculty.objects.all()
            context = {'title': 'Teacher', 'teachers': teachers, 'messages': [{'message': 'An error occurred!', 'tag': 'danger'}]}
            return render(request, 'teachers.html', context=context)
        print(teacher, 'teacher deleted successfully!')
        teachers = Faculty.objects.all()
        context = {'title': 'Teacher', 'teachers': teachers, 'messages': [{'message': 'Teacher deleted successfully!', 'tag': 'success'}]}
        return render(request, 'teachers.html', context=context)
    teachers = Faculty.objects.all()
    context = {'title': 'Teacher', 'teachers': teachers}
    return render(request, 'teachers.html', context=context)


# def teacher_info(request, id):
#     teacher = Faculty.objects.get(id=id)
#     context = {'title': 'Teacher', 'teacher': teacher}
#     return render(request, 'teacher/teacher-info.html', context=context)