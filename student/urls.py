from django.urls import path
from student.views import student, update_student, delete_student, student_info

urlpatterns = [
    path('students/', student, name='student'),
    path('student/<str:id>/', student_info, name='student-info'),
    path('students/update-student/', update_student, name='update-student'),
    path('students/delete-student/', delete_student, name='delete-student'),
    
]