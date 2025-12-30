from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from TaskManagementApp.models import Teams, Task, Profile
import random
from datetime import datetime, timedelta
# CleanUpDB: python manage.py flush
# Usage: python manage.py seed_data
class Command(BaseCommand):
    help = 'Populates the database with sample data including descriptions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate data...")

        # 1. Create Teams
        team_names = ["Backend Development", "UI/UX Design", "Digital Marketing", "Product Management", "Cyber Security"]
        teams = []
        for name in team_names:
            team, _ = Teams.objects.get_or_create(Name=name)
            teams.append(team)

        # 2. Create Users and Profiles
        users_data = [
            ("lea_dev", "Backend Development"),
            ("rachel_design", "UI/UX Design"),
            ("sara_prod", "Product Management"),
            ("moshe_sec", "Cyber Security"),
        ]

        for username, t_name in users_data:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password("task1234")
                user.save()

            team = Teams.objects.get(Name=t_name)
            profile, _ = Profile.objects.get_or_create(User=user)
            profile.team = team
            profile.role = "EMPLOYEE"
            profile.save()

        # 3. Create Diverse Tasks with Descriptions
        # הוספתי איבר שלישי לכל טאפל - התיאור של המשימה
        task_templates = [
            ("Fix Server Bug", "Backend Development", "Investigate and resolve the critical 500 error reported in the production API."),
            ("Design New Landing Page", "UI/UX Design", "Create a high-fidelity prototype for the upcoming winter marketing campaign."),
            ("Write Requirements Document", "Product Management", "Draft the initial technical requirements for the new user dashboard feature."),
            ("Periodic Penetration Test", "Cyber Security", "Perform a comprehensive security audit on the external authentication gateway."),
            ("Database Optimization", "Backend Development", "Analyze slow queries and implement necessary indexing to improve system latency."),
            ("User Research for Dark Mode", "UI/UX Design", "Conduct a survey among top users to gather feedback on the new dark mode color palette."),
            ("Client Synchronization Meeting", "Product Management", "Prepare the quarterly roadmap presentation for the enterprise client stakeholders."),
            ("Update Django Version", "Backend Development", "Upgrade the project framework to the latest stable version and fix deprecated functions."),
        ]

        statuses = ['NEW', 'IN_PROGRESS', 'COMPLETED']

        for i in range(20):
            # פירוק הטאפל ל-3 משתנים
            name_base, t_name, description = random.choice(task_templates)
            team = Teams.objects.get(Name=t_name)

            Task.objects.create(
                Name=f"{name_base} #{i + 1}",
                Description=description,  # הוספת התיאור למודל
                Teams=team,
                Status=random.choice(statuses),
                Due_Date=datetime.now().date() + timedelta(days=random.randint(1, 14)),
                AssignedUser=random.choice([None, User.objects.get(username="lea_dev")])
            )

        self.stdout.write(self.style.SUCCESS("Database populated successfully with English names and descriptions!"))