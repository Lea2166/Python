from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from TaskManagementApp.models import Teams, Task, Profile
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'ממלא את הדאטה-בייס בנתונים יפים לבדיקה'

    def handle(self, *args, **kwargs):
        self.stdout.write("מתחיל במילוי נתונים...")

        # 1. יצירת צוותים
        team_names = ["פיתוח Backend", "עיצוב UI/UX", "שיווק דיגיטלי", "ניהול מוצר", "אבטחת מידע"]
        teams = []
        for name in team_names:
            team, _ = Teams.objects.get_or_create(Name=name)
            teams.append(team)

        # 2. יצירת משתמשים ופרופילים
        users_data = [
            ("lea_dev", "פיתוח Backend"),
            ("rachel_design", "עיצוב UI/UX"),
            ("sara_prod", "ניהול מוצר"),
            ("moshe_sec", "אבטחת מידע"),
        ]

        for username, t_name in users_data:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password("task1234")
                user.save()

            # עדכון פרופיל
            team = Teams.objects.get(Name=t_name)
            profile, _ = Profile.objects.get_or_create(User=user)
            profile.team = team
            profile.role = "EMPLOYEE"
            profile.save()

        # 3. יצירת משימות מגוונות
        task_templates = [
            ("תיקון באג בשרת", "פיתוח Backend"),
            ("עיצוב דף נחיתה חדש", "עיצוב UI/UX"),
            ("כתיבת מסמך דרישות", "ניהול מוצר"),
            ("בדיקת חדירות תקופתית", "אבטחת מידע"),
            ("אופטימיזציה של ה-DB", "פיתוח Backend"),
            ("מחקר משתמשים לממשק הכהה", "עיצוב UI/UX"),
            ("סנכרון מול הלקוח", "ניהול מוצר"),
            ("עדכון גרסת Django", "פיתוח Backend"),
        ]

        statuses = ['NEW', 'IN_PROGRESS', 'COMPLETED']

        for i in range(20):  # ניצור 20 משימות
            name_base, t_name = random.choice(task_templates)
            team = Teams.objects.get(Name=t_name)

            Task.objects.create(
                Name=f"{name_base} #{i + 1}",
                Teams=team,
                Status=random.choice(statuses),
                Due_Date=datetime.now().date() + timedelta(days=random.randint(1, 14)),
                # חלק מהמשימות משויכות וחלק לא
                AssignedUser=random.choice([None, User.objects.get(username="lea_dev")])
            )

        self.stdout.write(self.style.SUCCESS("הדאטה-בייס התמלא בהצלחה!"))