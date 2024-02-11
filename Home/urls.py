from django.urls import path
from .views import HomePage, facultyDashboard, studentDashboard

urlpatterns = [
    path('', HomePage.as_view, name='home'),
    path('faculty_dashboard/', facultyDashboard, name='faculty_dashboard'),
    path('student_dashboard/', studentDashboard, name='student_dashboard')
]
