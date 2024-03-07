from django.urls import path
from student.views import student, update_student, delete_student

urlpatterns = [
    path('students/', student, name='student'),
    path('student/<int:id>/', student, name='student-info'),
    path('students/update-student/', update_student, name='update-student'),
    path('students/delete-student/', delete_student, name='delete-student'),
]