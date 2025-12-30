from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User

# Create your models here.
USER_ROLES = [
    ('ADMIN', 'מנהל'),
    ('EMPLOYEE', 'עובד'),
]
TASK_STATUS = [
    ('NEW', 'חדש'),
    ('IN_PROGRESS', 'בתהליך'),
    ('COMPLETED', 'הושלם'),
]
class Teams(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Name) # מחזיר את שם הצוות

class Profile(models.Model):
    Id = models.AutoField(primary_key=True)
    User = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name="Team")
    role = models.CharField(choices=USER_ROLES, max_length=20)

    def __str__(self):
        return str(self.User.username) # מחזיר את שם המשתמש

class Task(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Due_Date = models.DateField()
    Status = models.CharField(choices=TASK_STATUS, max_length=20)
    AssignedUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Name) # מחזיר את שם המשימה


