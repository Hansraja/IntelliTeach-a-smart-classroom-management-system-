from django.urls import path
from .views import home_login, studentDashboard, Images
from Admin.views import add_notice

urlpatterns = [
    path('', home_login, name='home'),
    path('', studentDashboard, name='student_dashboard'),
    path('add_notice/', add_notice, name='add_notice'),
    # path('media/<path:path>', Images, name='images')
]
