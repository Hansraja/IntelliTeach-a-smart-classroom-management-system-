from django.urls import path
from .views import home_login, studentDashboard, Images

urlpatterns = [
    path('', home_login, name='home'),
    path('', studentDashboard, name='student_dashboard'),
    path('media/<path:path>', Images, name='images')
]
