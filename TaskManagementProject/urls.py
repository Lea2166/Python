from django.contrib import admin
from django.urls import path
from TaskManagementApp import views
from django.views.generic import RedirectView # ייבוא חדש לצורך הפניה

urlpatterns = [
    # הפניה אוטומטית מהשורש לדף ההתחברות
    path('', RedirectView.as_view(url='login/'), name='root-redirect'),

    path('admin/', admin.site.urls),
    path('alltasks/', views.task_list, name='alltasks'),
    path('complete_profile', views.complete_profile, name='complete_profile'),
    path('claim-task/<int:task_id>/', views.claim_task, name='claim_task'),
    path('finish_task/<int:task_id>/', views.finish_task, name='finish_task'),

    # דפי התחברות וניהול
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('add/', views.add_task, name='add_task'),
    
    # אל תשכחו להוריד את ה-Comments מהעריכה והמחיקה כשתהיו מוכנות:
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('logout/', views.logout_view, name='logout'),
]