from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, Profile,Teams
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
@login_required
def task_list(request):
    user_profile = request.user.profile
    user_team = user_profile.team
    tasks = Task.objects.filter(Teams=user_team)
    for task in tasks:
        print(task)
    context = {
        'tasks': tasks,
        'team_name': user_team.Name,
        'user_role': user_profile.role
    }
    return render(request, 'AllTasks.html', context)

def login_view(request):
    if request.method == 'POST':
        # שליחת נתוני הטופס לאימות
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # שליפת המשתמש שאומת בהצלחה
            user = form.get_user()
            auth_login(request, user)
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
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})