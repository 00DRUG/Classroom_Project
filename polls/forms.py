from django import forms
from .models import Homework, Submission

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'assigned_date', 'due_date', 'file']  # Add file field

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

# Form for teacher to provide feedback
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'comments', 'allow_resubmission']
