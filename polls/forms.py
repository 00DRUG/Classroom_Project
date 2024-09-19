from django import forms
from .models import Homework, Submission, CustomUser

from django import forms
from .models import Homework

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'assigned_date', 'due_date', 'file', 'students']
    students = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(is_student=True), required=True, widget=forms.CheckboxSelectMultiple)

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