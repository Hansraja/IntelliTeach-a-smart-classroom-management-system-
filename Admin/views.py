from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import AuthUser, Faculty
from Home.models import Student_Notice, Time_Table, Attendance
import json
from django.conf import settings
import pandas as pd
import datetime
from urllib.parse import quote, unquote

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

from django.core.mail import send_mail
@login_required(login_url='home')
def delete_notice(request, id):
    if not request.user.is_faculty or not request.user.is_hod:
        return redirect('home')
    try:
        send_mail(from_email=settings.DEFAULT_FROM_EMAIL,  subject='Hello Email from IntelliTeach',  recipient_list=['ravikantsaini047@gmail.com'], message='Hello I am From IntelliTeach')
        notice = Student_Notice.objects.get(id=int(id))
        notice.delete()
        return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')
    
@login_required(login_url='home')
def time_table(request):
    if request.method == 'POST':
        if not request.user.is_faculty or not request.user.is_hod:
            return redirect('home')
        day = request.POST.get('day', None)
        time_from = request.POST.get('from', None)
        time_to = request.POST.get('to', None)
        subject = request.POST.get('subject', None)
        try:
            Time_Table.objects.create(day=day, time_from=time_from, time_to=time_to, subject=subject)
            return redirect('time_table')
        except Exception as e:
            print(e)
            return redirect('time_table')
    
     # Query the Time_Table objects
    time_table_objects = Time_Table.objects.all() or []

    if not time_table_objects:
        return render(request=request, template_name='table.html', context={'title': f'Time Table - {settings.APP_NAME}'})
    
    # Create a DataFrame from the queryset
    df = pd.DataFrame(list(time_table_objects.values('day', 'time_from', 'time_to', 'subject')))

    # Convert time_from and time_to to strings
    df['time_from'] = df['time_from'].apply(lambda x: x.strftime('%I:%M %p') if x else None)
    df['time_to'] = df['time_to'].apply(lambda x: x.strftime('%I:%M %p') if x else None)

    df['time_range'] = df['time_from'] + ' - ' + df['time_to']

    # Define the desired order of time ranges
    time_range_order = settings.TIME_RANGE_ORDER

    day_order = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday'
    ]

    # Pivot the DataFrame to rearrange the data
    df_pivot = df.pivot(index='day', columns='time_range', values='subject')

    # Reorder columns according to the defined order
    df_pivot = df_pivot[time_range_order] if time_range_order else df_pivot

    # Sort days
    df_pivot = df_pivot.reindex(day_order)

    # Generate HTML table
    html_table = df_pivot.to_html(classes='table table-bordered', na_rep='', index_names=False, justify='center')

    context = {'html_table': html_table, 'title': f'Time table - {settings.APP_NAME}',}
    return render(request=request, template_name='table.html', context=context)


def update_time_table(request):
    if not request.user.is_faculty or not request.user.is_hod:
        return redirect('home')
    if request.method == 'POST':
        data = request.body
        data = json.loads(data) if data else {}
        for obj in data:
            _id = obj.get('pk', None)
            day = obj.get('day', None)
            time_from = datetime.datetime.strptime(obj.get('from', None), '%H:%M').time() if obj.get('from', None) else None
            time_to = datetime.datetime.strptime(obj.get('to', None), '%H:%M').time() if obj.get('to', None) else None
            subject = obj.get('subject', None)
            if _id:
                if day and time_from and time_to and subject:
                    try:
                        time_table = Time_Table.objects.get(id=_id)
                        time_table.day = day
                        time_table.time_from = time_from
                        time_table.time_to = time_to
                        time_table.subject = subject
                        time_table.save()
                    except Exception as e:
                        print(e)
                        return JsonResponse({'success': False, 'message': 'An error occurred while updating time table'})
                elif not day or not time_from or not time_to or not subject:
                    Time_Table.objects.get(id=_id).delete()
            else:
                return JsonResponse({'success': False, 'message': 'Invalid request'})
        return JsonResponse({'success': True, 'message': 'Time table updated successfully'})
    
    time_table_objects = Time_Table.objects.all()

    arr = []

    for obj in time_table_objects:
        arr.append({
            'id': obj.id,
            'day': obj.day,
            'time_from': obj.time_from.strftime('%H:%M') if obj.time_from else '',
            'time_to': obj.time_to.strftime('%H:%M') if obj.time_to else '',
            'subject': obj.subject
        })

    return render(request, 'update_table.html', {'time_table': arr, 'title': f'Time Table - {settings.APP_NAME}',})



def attendance_view(request):
    if not request.user.is_faculty or not request.user.is_hod:
        return redirect('home')
    att = Attendance.objects.all()
    attendance_records = Attendance.objects.all()   
    time_table_qs = Time_Table.objects.all()

    # Create lists to store data for each column
    days = []
    dates = []
    subjects = []
    time_ranges = []

    # Populate lists with time table data
    for tt in time_table_qs:
        days.append(tt.day)
        dates.append(tt.created_at.date())
        subjects.append(tt.subject)
        time_range = f"{tt.time_from.strftime('%I:%M %p') if tt.time_from else ''} - {tt.time_to.strftime('%I:%M %p') if tt.time_to else ''}"
        time_ranges.append(time_range)

    # Create DataFrame for time table
    time_table_df = pd.DataFrame({
        'Day': days,
        'Date': dates,
        'Subject': subjects,
        'Time Range': time_ranges
    })

    def add_link(row):
        day = row['Day']
        date = row['Date']
        subject = row['Subject']
        time_range = row['Time Range']
        link = f'<button class="btn btn-info btn-sm"> <a href="/attendance/{quote(string=subject)}" target="_blank">View</a> </button>'
        return link
    
    time_table_df['View'] = time_table_df.apply(add_link, axis=1)

    # # Get unique dates from the attendance records
    # dates = sorted(set(attendance_record.created_at.date() for attendance_record in attendance_records))

    # # Create a DataFrame with student names as index and dates as columns
    # student_names = [attendance.student.user.get_full_name() for attendance in attendance_records]
    # attendance_df = pd.DataFrame(index=student_names, columns=dates)

    # # Fill the DataFrame with 'P' for present and 'A' for absent
    # for attendance in attendance_records:
    #     date = attendance.created_at.date()
    #     student_name = attendance.student.user.get_full_name()
    #     attendance_df.at[student_name, date] = 'P' if attendance.status else 'A'

    # # Fill missing values with 'A' (Absent)
    # attendance_df.fillna('A', inplace=True)

    # # Populate the DataFrame according to the time table
    # for tt in time_table:
    #     date = tt.created_at.date()
    #     subject = tt.subject
    #     time_from = tt.time_from
    #     time_to = tt.time_to
    #     attendance_df[f"{date} {time_from} - {time_to} ({subject})"] = ' '

    # time_table = Time_Table.objects.all()

    # attendance_records = Attendance.objects.all()

    att = time_table_df.to_html(classes='table table-bordered', na_rep='', index_names=True, justify='center', escape=False)
    context = {'attendance': att, 'title': f'Attendance - {settings.APP_NAME}'}
    return render(request=request, template_name='settings/attendance-list.html', context=context)


def one_attendance_view(request, id):
    if not request.user.is_faculty or not request.user.is_hod:
        return redirect('home')
    try:
        tm = Time_Table.objects.get(subject=unquote(id))
        att = Attendance.objects.filter(time=tm)

        # Create a DataFrame to hold the attendance data
        data = []
        students = set()
        dates = set()
        for attendance in att:
            students.add(attendance.student.user.get_full_name())
            data.append({
                'Date': attendance.created_at.date(),
                'Student Name': attendance.student.user.get_full_name(),
                'Status': 'P' if attendance.status else 'A'
            })
            dates.add(attendance.created_at.date())

        # Create DataFrame
        df = pd.DataFrame(data)

        # Pivot the DataFrame to have dates as columns and students as rows
        pivot_df = df.pivot(index='Student Name', columns='Date', values='Status')

        # Reorder columns by date
        pivot_df = pivot_df[sorted(dates)]
        html_table = pivot_df.to_html(classes='table table-bordered', na_rep='', escape=False, justify='center', index_names=True, notebook=True, render_links=True)

        context = {'html_table': html_table, 'subject': tm.subject, 'title': f'Attendance - {settings.APP_NAME}'}
        return render(request=request, template_name='settings/one-attendance.html', context=context)
    except Exception as e:
        print(e)
        return render(request=request, template_name='settings/one-attendance.html', context={'emp':True, 'title': f'Attendance - {settings.APP_NAME}'})