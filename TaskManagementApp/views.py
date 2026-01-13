from contextlib import nullcontext

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .decorators import admin_only
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404


from django.contrib.auth.decorators import login_required
from .models import Task, Profile,Teams
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import TaskForm, AdminTaskForm,CompleteProfileForm
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in as " + request.user.username)
        return redirect('alltasks')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('alltasks')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(User=user)
            login(request, user)
            return redirect('alltasks')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def claim_task(request, task_id):
    task = get_object_or_404(Task, Id=task_id)

    task.AssignedUser = request.user
    task.Status = 'IN_PROGRESS'
    task.save()

    print(f"DEBUG: Task {task.Name} assigned to {request.user.username}")
    return redirect('alltasks')
@login_required
def finish_task(request, task_id):
    task = get_object_or_404(Task, Id=task_id)
    task.Status = 'COMPLETED'
    task.save()
    return redirect('alltasks')

@login_required
def task_list(request):
    user_profile = request.user.profile

    if user_profile.role == 'ADMIN':
        tasks = Task.objects.all().order_by('Due_Date')
        team_name = "All System Tasks"
    else:
        if user_profile.team is None and user_profile.role != 'ADMIN':
            return redirect(complete_profile)
        tasks = Task.objects.filter(Teams=user_profile.team).order_by('Due_Date')
        team_name = user_profile.team.Name

    owner_filter = request.GET.get('owner', 'all')
    if owner_filter == 'mine':
        tasks = tasks.filter(AssignedUser=request.user)

    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        tasks = tasks.filter(Status=status_filter)

    context = {
        'tasks': tasks,
        'team_name': team_name,
        'owner_filter': owner_filter,
        'status_filter': status_filter,
        'owner_options': [('all','All'), ('mine','Mine')],
        'status_options': [('all','All'), ('NEW','new'), ('IN_PROGRESS','in_progress'), ('COMPLETED','completed')],
        'user_role': user_profile.role,
    }
    return render(request, 'AllTasks.html', context)
@login_required
def complete_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        selected_role = request.POST.get('role')
        selected_team_id = request.POST.get('team')

        if selected_role:
            profile.role = selected_role
            if selected_role == 'EMPLOYEE' and selected_team_id:
                profile.team = Teams.objects.get(Id=selected_team_id)
            else:
                profile.team = None

            profile.save()
            return redirect('alltasks')

    all_teams = Teams.objects.all()
    return render(request, 'NoTeam.html', {
        'all_teams': all_teams,
        'user_name': request.user.username
    })
@login_required
@admin_only
def add_task(request):
    is_admin = request.user.profile.role == 'ADMIN'
    form_class = AdminTaskForm if is_admin else TaskForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if not is_admin:
                task.Teams = request.user.profile.team
            task.Status = 'NEW'
            task.save()
            return redirect('alltasks')
    else:
        form = form_class()
    return render(request, 'task_form.html', {'form': form, 'title': 'Create New Task'})
@login_required
@admin_only
def edit_task(request, task_id):
    task = get_object_or_404(Task, Id=task_id)

    if task.AssignedUser:
        return redirect('alltasks')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('alltasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'title': 'Task Editor'})
@admin_only
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, Id=task_id)

    if not task.AssignedUser:
        task.delete()

    return redirect('alltasks')
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "התנתקת מהמערכת בהצלחה.")
    return redirect('/')

from django.http import JsonResponse

@login_required
@admin_only
def get_employees_by_team(request):
    team_id = request.GET.get('team_id')
    # שליפת כל המשתמשים שמשויכים לצוות הספציפי דרך ה-Profile
    employees = User.objects.filter(profile__team_id=team_id, profile__role='EMPLOYEE').values('id', 'username')
    return JsonResponse(list(employees), safe=False)
from django.shortcuts import render

def error_404(request, exception):
    return render(request, 'error_page.html', {
        'status_code': '404',
        'title': 'Page Not Found',
        'message': 'Sorry, we could not find the page you were looking for.'
    }, status=404)

def error_500(request):
    return render(request, 'error_page.html', {
        'status_code': '500',
        'title': 'Server Error',
        'message': 'An internal server error occurred, we are working on it!'
    }, status=500)

def error_403(request,exception=None, reason=""):
    return render(request, 'error_page.html', {
        'status_code': '403',
        'title': 'Permission Denied',
        'message': 'You do not have permission to access this page (or your token has expired).'
    }, status=403)