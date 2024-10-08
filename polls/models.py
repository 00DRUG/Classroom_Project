# polls/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    age = models.IntegerField(null=True, blank=True)  # Add age field here
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")

    def __str__(self):
        return self.username


class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    file = models.FileField(upload_to='homework_files/', null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='homeworks')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='homework_assigned', blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="homeworks")

    def __str__(self):
        return self.title


class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('returned', 'Returned for redo'),
        ('graded', 'Graded'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='homework_submissions/')
    submitted_on = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    allow_resubmission = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"
