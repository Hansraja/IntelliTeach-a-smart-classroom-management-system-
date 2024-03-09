from django.urls import path
from .views import delete_topic, facultyDashboard, faculty_Profile, assignment_list, single_assignment, update_assignment, important_topics, delete_topic

urlpatterns = [
    path('', facultyDashboard, name='teacher_dashboard'),
    path('assignments/', assignment_list, name='assignments'),
    path('assignment/<int:id>', single_assignment, name='assignment'),
    path('assignment/<int:assignment_id>/update', update_assignment, name='update-assignment'),
    path('topics', important_topics, name='topics'),
    path('topic/<int:id>/delete', delete_topic, name='delete-topic'),
    path('profile', faculty_Profile, name='teacher_profile' ),
]
