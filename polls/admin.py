# polls/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Custom form to create users with additional fields
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'is_student', 'is_teacher', 'age')  # Add custom fields here


# Custom form to change users with additional fields
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'is_student', 'is_teacher', 'age')  # Add custom fields here


# Custom UserAdmin to handle CustomUser
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # The form used to create a new user
    form = CustomUserChangeForm  # The form used to change an existing user
    model = CustomUser

    # Specify the fields to display in the Django admin interface
    list_display = ['username', 'email', 'is_student', 'is_teacher', 'age', 'is_staff', 'is_superuser']

    # Fields to show in the User edit form in the admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_teacher', 'age')}),  # Add custom fields here
    )

    # Fields to show when adding a new User
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'is_student', 'is_teacher', 'age')}),  # Add custom fields here
    )


admin.site.register(CustomUser, CustomUserAdmin)
