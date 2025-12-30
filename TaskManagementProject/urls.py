"""
URL configuration for TaskManagementProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TaskManagementApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alltasks/',views.task_list,name='alltasks'),
    path('NoTeam',views.NoTeams,name='NoTeam'),
path('claim-task/<int:task_id>/', views.claim_task, name='claim_task'),
path('finish_task/<int:task_id>/', views.finish_task, name='finish_task'),

    # דף התחברות מוכן של דג'אנגו
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
