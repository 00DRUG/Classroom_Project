# polls/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Group
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'is_student', 'is_teacher', 'age', 'group')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'is_student', 'is_teacher', 'age', 'group')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['username', 'email', 'is_student', 'is_teacher', 'age', 'is_staff', 'is_superuser']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_teacher', 'age', 'group')}),
    )

    # Fields to show when adding a new User
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'is_student', 'is_teacher', 'age', 'group')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
