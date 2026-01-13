from django.db import models
from django.contrib.auth.models import User

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
        return str(self.Name)

class Profile(models.Model):
    Id = models.AutoField(primary_key=True)
    User = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name="Team",null=True, blank=True)
    role = models.CharField(choices=USER_ROLES, max_length=20,default="EMPLOYEE")

    def __str__(self):
        return str(self.User.username)

class Task(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Due_Date = models.DateField()
    Status = models.CharField(choices=TASK_STATUS, max_length=20,default="NEW")
    AssignedUser = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    Teams = models.ForeignKey(Teams, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Name)