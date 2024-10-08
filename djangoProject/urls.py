from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import polls.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', polls.views.unified_login),
    path('student/dashboard/', polls.views.student_dashboard, name='student_dashboard'),  # Name is 'classroom_hub'
    path('homework/<int:homework_id>/submit/', polls.views.upload_submission, name='upload_submission'),
    path('calendar/', polls.views.homework_calendar_view, name='homework_calendar'),
    path('teacher/dashboard/', polls.views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/homework/add/', polls.views.add_homework, name='add_homework'),
    path('teacher/homework/add/', polls.views.add_homework, name='add_homework'),
    path('teacher/homework/<int:homework_id>/submissions/', polls.views.view_submissions, name='view_submissions'),
    path('teacher/submission/<int:submission_id>/feedback/', polls.views.give_feedback, name='give_feedback'),
    path('teacher/homework/<int:homework_id>/delete/', polls.views.delete_homework, name='delete_homework'),
    path('logout/', polls.views.unified_login, name='logout'),
    path('profile/<int:user_id>/', polls.views.profile_view, name='profile_view'),
    path('profile/edit/', polls.views.edit_profile, name='edit_profile'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
