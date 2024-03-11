from django.conf import settings
from django.db import models
from Admin.models import AuthUser, Faculty, Student
from django.core.mail import send_mail
# Create your models here.

class Teacher_Messages(models.Model):
    admin = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Faculty, related_name='teacher_messages')
    message = models.CharField(max_length=10000, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_messages'

    def __str__(self):
        return self.message
    

class Student_Notice(models.Model):
    admin = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_messages', null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    message = models.CharField(max_length=10000, blank=True, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'student_messages'

    def send_to_email(self):
        try:
            for student in Student.objects.all():
                send_mail(  
                    f"{self.title} - {settings.APP_NAME}",
                    self.message,
                    settings.DEFAULT_FROM_EMAIL,
                    [student.user.email],
                    fail_silently=False,
                )
            for teacher in Faculty.objects.all():
                send_mail( 
                    f"{self.title} - {settings.APP_NAME}",
                    self.message,
                    settings.DEFAULT_FROM_EMAIL,
                    [teacher.user.email],
                    fail_silently=False,
                )
        except:
            pass

    def __str__(self):
        return self.message
    
class Student_Marks(models.Model):
    teacher = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='teacher_marks', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_marks', null=True, blank=True)
    mst1 = models.IntegerField(blank=True, null=True)
    mst2 = models.IntegerField(blank=True, null=True)
    assignment = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'student_marks'

    def send_to_email(self):
        pass

    def get_total_marks(self):
        mst1 = int(self.mst1) if self.mst1 else 0
        mst2 = int(self.mst2) if self.mst2 else 0
        assignment = int(self.assignment) if self.assignment else 0
        return mst1 + mst2 + assignment

    def __str__(self):
        return f"{self.student.user.get_full_name()} marks" # type: ignore
    
class Time_Table(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    teacher = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='teacher_timetable', null=True, blank=True)
    day = models.CharField(max_length=255, choices=DAY_CHOICES, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    class_name = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'time_table'

    def __str__(self):
        return self.teacher.user.first_name + ' ' + self.teacher.user.last_name + ' timetable' # type: ignore

    @staticmethod
    def get_table_structure():
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        table_structure = {}
        for day in days:
            classes = Time_Table.objects.filter(day=day)
            table_structure[day] = [c.class_name for c in classes]
        return table_structure
    

class Attendance(models.Model):
    teacher = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='teacher_attendance', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance', null=True, blank=True)
    time = models.ForeignKey(Time_Table, on_delete=models.CASCADE, related_name='time_attendance', null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance'

    def __str__(self):
        return self.teacher.user.first_name + ' ' + self.teacher.user.last_name + ' attendance' # type: ignore        def calculate_student_attendance_percentage(student_id):

    def calculate_student_attendance_percentage(self, student_id): 
        total_classes = Time_Table.objects.count()
        attended_classes = Attendance.objects.filter(student_id=student_id, status=True).count()
        attendance_percentage = (attended_classes / total_classes) * 100
        return attendance_percentage