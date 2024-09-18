from django.contrib.auth import authenticate, login
from django.shortcuts import  get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Homework, Submission
from .forms import HomeworkForm, SubmissionForm, FeedbackForm
from datetime import datetime, timezone
def unified_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_role = request.POST['role']
        remember_me = request.POST.get('remember_me', False)  # Get the Remember Me checkbox value

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if (user_role == 'student' and user.is_student) or (user_role == 'teacher' and user.is_teacher):
                login(request, user)

                if remember_me:  # If remember me is checked, set the session expiry to 30 days
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
                else:
                    request.session.set_expiry(0)  # Browser session only

                if user_role == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('teacher_dashboard')
    return render(request, 'unified_login.html')
@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')


@login_required
def student_dashboard(request):
    # Ensure that only students can access the student dashboard
    if not request.user.is_student:
        return redirect('teacher_dashboard')  # Redirect teachers to their dashboard

    # Get all homework assigned to the student
    homeworks = Homework.objects.filter(due_date__gte=datetime.now())  # Only show active homework
    # Get all submissions by the student
    submissions = Submission.objects.filter(student=request.user)

    homework_data = []

    for homework in homeworks:
        submission = submissions.filter(homework=homework).first()  # Get the first submission if it exists
        if not submission or submission.status in ['pending', 'returned']:
            homework_data.append({
                'homework': homework,
                'submission': submission,
                'resubmission_allowed': submission.allow_resubmission if submission else False,
            })

    context = {
        'homework_data': homework_data,
        'submissions': submissions,
    }
    return render(request, 'student_dashboard.html', context)


@login_required
def upload_submission(request, homework_id):
    homework = Homework.objects.get(id=homework_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.homework = homework
            submission.save()
            return redirect('student_dashboard')
    else:
        form = SubmissionForm()
    return render(request, 'upload_submission.html', {'form': form, 'homework': homework})


@login_required
def teacher_dashboard(request):
    # Ensure that only teachers can access the teacher dashboard
    if not request.user.is_teacher:
        return redirect('student_dashboard')  # Redirect students to their dashboard

    # Get all homework created by the teacher
    homeworks = Homework.objects.filter(teacher=request.user)

    context = {
        'homeworks': homeworks,
    }
    return render(request, 'teacher_dashboard.html', context)


@login_required
def add_homework(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.teacher = request.user
            homework.save()
            return redirect('teacher_dashboard')
    else:
        form = HomeworkForm()

    return render(request, 'add_homework.html', {'form': form})


@login_required
def homework_calendar(request):
    homeworks = Homework.objects.all()
    return render(request, 'homework_calendar.html', {'homeworks': homeworks})


@login_required
def give_feedback(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, homework__teacher=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=submission)
        if form.is_valid():
            feedback = form.save(commit=False)

            # If resubmission is allowed, mark the submission as "returned"
            if feedback.allow_resubmission:
                feedback.status = 'returned'
            else:
                feedback.status = 'graded'  # Otherwise, mark it as graded

            feedback.save()
            return redirect('view_submissions', homework_id=submission.homework.id)
    else:
        form = FeedbackForm(instance=submission)

    return render(request, 'give_feedback.html', {'form': form, 'submission': submission})
@login_required
def delete_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id, teacher=request.user)
    if request.method == 'POST':
        homework.delete()  # Delete the homework assignment
        return redirect('teacher_dashboard')
    return render(request, 'confirm_delete_homework.html', {'homework': homework})


@login_required
def view_submissions(request, homework_id):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    homework = get_object_or_404(Homework, id=homework_id, teacher=request.user)
    submissions = Submission.objects.filter(homework=homework)
    return render(request, 'view_submissions.html', {'homework': homework, 'submissions': submissions})
