from contextlib import nullcontext

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Profile,Teams
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import TaskForm, AdminTaskForm,CompleteProfileForm


@login_required
# def task_list(request):
#     user_profile = request.user.profile
#     user_team = user_profile.team
#     if user_team is None:
#         return redirect(complete_profile)
#
#     tasks = Task.objects.filter(Teams=user_team).order_by('Due_Date')
#
#     # לוגיקת סינון
#     owner_filter = request.GET.get('owner', 'all')
#     if owner_filter == 'mine':
#         tasks = tasks.filter(AssignedUser=request.user)
#
#     status_filter = request.GET.get('status', 'all')
#     if status_filter != 'all':
#         tasks = tasks.filter(Status=status_filter)
#
#     # רשימות סינון למניעת שגיאת TemplateSyntaxError
#     owner_options = [('all', 'כל הצוות'), ('mine', 'המשימות שלי')]
#     status_options = [
#         ('all', 'הכל'),
#         ('NEW', 'חדש'),
#         ('IN_PROGRESS', 'בביצוע'),
#         ('COMPLETED', 'הושלם')
#     ]
#
#     context = {
#         'tasks': tasks,
#         'team_name': user_team.Name,
#         'owner_filter': owner_filter,
#         'status_filter': status_filter,
#         'owner_options': owner_options,
#         'status_options': status_options,
#         'user_role': user_profile.role,
#     }
#     return render(request, 'AllTasks.html', context)
#

def login_view(request):
    if request.method == 'POST':
        # שליחת נתוני הטופס לאימות
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # שליפת המשתמש שאומת בהצלחה
            user = form.get_user()
            login(request, user)
            # מעבר לדף המשימות של הצוות
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


def claim_task(request, task_id):
    task = get_object_or_404(Task, Id=task_id)

    task.AssignedUser = request.user
    task.Status = 'IN_PROGRESS'
    task.save()

    print(f"DEBUG: Task {task.Name} assigned to {request.user.username}")
    return redirect('alltasks')
def finish_task(request, task_id):
    task = get_object_or_404(Task, Id=task_id)
    task.Status = 'COMPLETED'
    task.save()
    return redirect('alltasks')


def task_list(request):
    user_profile = request.user.profile

    # מנהל רואה הכל כברירת מחדל, עובד רואה רק את הצוות שלו
    if user_profile.role == 'ADMIN':
        tasks = Task.objects.all().order_by('Due_Date')
        team_name = "כל המשימות במערכת"
    else:
        if user_profile.team is None and user_profile.role != 'ADMIN':
            return redirect(complete_profile)
        tasks = Task.objects.filter(Teams=user_profile.team).order_by('Due_Date')
        team_name = user_profile.team.Name

    # לוגיקת סינונים (נשארת דומה, רק מוסיפים אפשרות לסינון צוות למנהל אם תרצו בעתיד)
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
        'owner_options': [('all', 'הכל'), ('mine', 'שלי')],
        'status_options': [('all', 'הכל'), ('NEW', 'חדש'), ('IN_PROGRESS', 'בביצוע'), ('COMPLETED', 'הושלם')],
        'user_role': user_profile.role,
    }
    return render(request, 'AllTasks.html', context)


@login_required
@login_required
def complete_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        selected_role = request.POST.get('role')
        selected_team_id = request.POST.get('team')

        if selected_role:
            profile.role = selected_role
            # אם הוא עובד - נשמור את הצוות. אם הוא מנהל - נשמור None
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
    return render(request, 'task_form.html', {'form': form, 'title': 'יצירת משימה חדשה'})


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
    return render(request, 'task_form.html', {'form': form, 'title': 'עריכת משימה'})

@login_required
def delete_task(request, task_id):
    """מחיקת משימה - רק אם לא משויכת לאף עובד"""
    task = get_object_or_404(Task, Id=task_id)

    # בדיקה שהמשימה לא משויכת ושהמשתמש מנהל (או לפי הצורך שלכן)
    if not task.AssignedUser:
        task.delete()

    return redirect('alltasks')