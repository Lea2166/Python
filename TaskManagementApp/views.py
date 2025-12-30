
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, Profile

@login_required
def task_list(request):
    user_profile = request.user.profile
    user_team = user_profile.team
    tasks = Task.objects.filter(Teams=user_team)
    context = {
        'tasks': tasks,
        'team_name': user_team.Name,
        'user_role': user_profile.role  # נשתמש בזה ב-HTML כדי להציג כפתורים שונים למנהל/עובד
    }
    return render(request, 'AllTasks.html', context)

