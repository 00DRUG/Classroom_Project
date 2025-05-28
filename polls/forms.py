# polls/forms.py

from django import forms
from .models import Homework, Submission, CustomUser, Group

class HomeworkForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(is_student=True),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select
    )

    class Meta:
        model = Homework
        fields = ['title', 'description', 'assigned_date', 'due_date', 'file', 'students', 'group']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'comments', 'allow_resubmission']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'bio', 'age']
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # Admin must approve
        if commit:
            user.save()
        return user
