from django.contrib.auth import authenticate, login
from django.shortcuts import  get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Homework, Submission
from .forms import HomeworkForm, SubmissionForm, FeedbackForm, ProfileForm
from datetime import datetime, timezone
from .models import CustomUser
def unified_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_role = request.POST['role']
        remember_me = request.POST.get('remember_me', False)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if (user_role == 'student' and user.is_student) or (user_role == 'teacher' and user.is_teacher):
                login(request, user)

                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.set_expiry(0)

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
    if not request.user.is_student:
        return redirect('teacher_dashboard')


    homeworks = Homework.objects.filter(students=request.user, due_date__gte=datetime.now())

    print(f"Number of homeworks fetched for student {request.user.username}: {homeworks.count()}")  # Debugging line

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
    homework = get_object_or_404(Homework, id=homework_id)


    if not request.user.is_student:
        return redirect('teacher_dashboard')


    submission, created = Submission.objects.get_or_create(homework=homework, student=request.user)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.submitted_on = datetime.now()
            new_submission.status = 'pending'
            new_submission.allow_resubmission = False
            new_submission.save()

            return redirect('student_dashboard')
    else:
        form = SubmissionForm(instance=submission)

    return render(request, 'upload_submission.html', {'form': form, 'homework': homework})


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

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

            selected_group = form.cleaned_data['group']
            selected_students = form.cleaned_data['students']


            if selected_group:
                group_students = selected_group.members.filter(is_student=True)
                homework.save()
                homework.students.set(group_students)
            else:

                homework.save()
                homework.students.set(selected_students)

            return redirect('teacher_dashboard')
    else:
        form = HomeworkForm()

    return render(request, 'add_homework.html', {'form': form})
@login_required
def homework_calendar(request):
    homeworks = Homework.objects.all()
    return render(request, 'homework_calendar.html', {'homeworks': homeworks})

@login_required
def profile_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'profile.html', {'user': user})
@login_required
def give_feedback(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, homework__teacher=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=submission)
        if form.is_valid():
            feedback = form.save(commit=False)

            if feedback.allow_resubmission:
                feedback.status = 'returned'
            else:
                feedback.status = 'graded'

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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view', user_id=request.user.id)
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
@login_required
def homework_calendar_view(request):
    # Fetch all homework for the logged-in student or teacher
    if request.user.is_teacher:
        homeworks = Homework.objects.filter(teacher=request.user)
    elif request.user.is_student:
        homeworks = Homework.objects.filter(students=request.user)
    else:
        homeworks = []

    context = {
        'homeworks': homeworks,
    }
    return render(request, 'homework_calendar.html', context)
