from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.unified_login, name='unified_login'),
    path('student/dashboard/', views.classroom_hub_view, name='classroom_hub'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
