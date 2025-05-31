# polls/forms.py

from django import forms
from .models import Homework, Submission, CustomUser, Group
from django.forms.widgets import ClearableFileInput
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
    assigned_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'id_assigned_date'}),
        required=True
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'id_due_date'}),
        required=True
    )

    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'assigned_date', 'due_date', 'file', 'students', 'group']

    def clean(self):
        cleaned_data = super().clean()
        students = cleaned_data.get('students')
        group = cleaned_data.get('group')

        if not students and not group:
            raise forms.ValidationError("Please select either a group or individual students.")
        return cleaned_data




class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['comments_student']
        exclude = ['file']
class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class SubmissionFilesForm(forms.Form):
    files = forms.FileField(
        widget=MultiFileInput(),
        required=False,
        label='Upload files',
    )



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'comments_teacher', 'allow_resubmission']
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
