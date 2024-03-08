from django.shortcuts import redirect, render
from django.http import HttpResponseServerError
from Admin.models import Student, AuthUser
from django.core.exceptions import ValidationError
import datetime


def student(request, context={}):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        father_name = request.POST.get('father_name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        mobile = request.POST.get('mobile', None)
        roll_number = request.POST.get('roll_number', None)
        image = request.FILES.get('image', None)
        dob = request.POST.get('dob', None)
        dob_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        dob_formatted = dob_date.strftime("%Y-%m-%d")
        try:
            user = AuthUser.objects.create(email=email, first_name=first_name, last_name=last_name, is_student=True, picture=image)
            user.set_password(password)
            student = Student.objects.create(user=user, roll_number=roll_number, dob=dob_formatted, father_name=father_name, mobile=mobile)
            student.send_welcome_email(password)
        except ValidationError as e:
            try:
                user.delete() if user else None
            except UnboundLocalError as e:
                pass
            return HttpResponseServerError("Something went wrong, try again.")
        except Exception as e:
            try:
                user.delete() if user else None
            except UnboundLocalError as e:
                pass
            students = Student.objects.all()
            context = {'title': 'Teacher', 'students': students, 'messages': [{'message': 'An error occurred!', 'tag': 'danger'}]}
            return render(request, 'student/index.html', context=context)
        students = Student.objects.all()
        context = {'title': 'Teacher', 'students': students, **context}
        return render(request, 'student/index.html', context=context)

    students = Student.objects.all()
    context = {'title': 'Teacher', 'students': students}
    return render(request, 'student/index.html', context=context)


def update_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('id', None)
        first_name = request.POST.get('first_name', None)
        father_name = request.POST.get('father_name', None)
        last_name = request.POST.get('last_name', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        roll_number = request.POST.get('roll_number', None)
        image = request.FILES.get('image', None)
        dob = request.POST.get('dob', None)
        try:
            student = Student.objects.get(id=student_id)
            # student.roll_number = roll_number if roll_number else student.roll_number
            student.dob = dob if dob else student.dob
            # student.user.email = email if email else student.user.email
            student.user.first_name = first_name if first_name else student.user.first_name
            student.user.last_name = last_name if last_name else student.user.last_name
            student.user.picture = image if image else student.user.picture # type: ignore
            student.father_name = father_name if father_name else student.father_name
            student.mobile = mobile if mobile else student.mobile
            student.user.save()
            student.save()
        except ValidationError as e:
            return HttpResponseServerError("Something went wrong, try again.")
        except Exception as e:
            students = Student.objects.all()
            context = {'title': 'Teacher', 'students': students, 'messages': [{'message': 'An error occurred!', 'tag': 'danger'}]}
            return render(request, 'student/index.html', context=context)
        students = Student.objects.all()
        context = {'title': 'Teacher', 'students': students, 'messages': [{'message': 'Student updated successfully!', 'tag': 'success'}]}
        return render(request, 'student/index.html', context=context)
    students = Student.objects.all()
    context = {'title': 'Teacher', 'students': students}
    return render(request, 'student/index.html', context=context)

def delete_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('id', None)
        try:
            student = Student.objects.get(id=student_id)
            student.user.delete_account_email()
            student.user.delete()
        except ValidationError as e:
            return HttpResponseServerError("Something went wrong, try again.")
        except Exception as e:
            students = Student.objects.all()
            context = {'title': 'Teacher', 'students': students, 'messages': [{'message': 'An error occurred!', 'tag': 'danger'}]}
            return render(request, 'student/index.html', context=context)
        students = Student.objects.all()
        context = {'title': 'Teacher', 'students': students, 'messages': [{'message': 'Student deleted successfully!', 'tag': 'success'}]}
        return render(request, 'student/index.html', context=context)
    students = Student.objects.all()
    context = {'title': 'Teacher', 'students': students}
    return render(request, 'student/index.html', context=context)


def student_info(request, id):
    try:
        student = Student.objects.get(roll_number=id)
        context = {'title': 'Teacher', 'student': student}
        return render(request, 'student/single.html', context=context)
    except Exception as e:
        students = Student.objects.all()
        context = {'title': 'Teacher', 'students': students, 'messages': [{'message': 'Student not found!', 'tag': 'danger'}]}
        return render(request, 'student/index.html', context=context)