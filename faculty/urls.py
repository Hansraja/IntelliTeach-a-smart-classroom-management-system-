from django.urls import path
from .views import facultyDashboard, faculty_Profile

urlpatterns = [
    path('', facultyDashboard, name='faculty_dashboard'),
    path('profile', faculty_Profile, name='faculty_profile' )
]
