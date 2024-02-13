from django.urls import path
from .views import HomePage, studentDashboard, Images

urlpatterns = [
    path('', HomePage.as_view, name='home'),
    path('student_dashboard/', studentDashboard, name='student_dashboard'),
    path('media/<path:path>', Images, name='images')
]
