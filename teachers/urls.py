from django.urls import path
from .views import facultyDashboard, faculty_Profile

urlpatterns = [
    path('', facultyDashboard, name='teacher_dashboard'),
    path('profile', faculty_Profile, name='teacher_profile' ),
]
