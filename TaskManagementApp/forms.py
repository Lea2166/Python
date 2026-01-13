from django import forms
from .models import Task, Teams, Profile
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['Name', 'Description', 'Due_Date']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 outline-none'}),
            'Description': forms.Textarea(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 outline-none', 'rows': 3}),
            # הגדרת לוח השנה
            'Due_Date': forms.DateInput(attrs={
    'class': 'bg-slate-800 border border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 outline-none transition-all custom-calendar-input',
    'type': 'date',
    'placeholder': 'Select due date...'
}),
        }
class AdminTaskForm(forms.ModelForm):
    AssignedUser = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Assign to employee",
        widget=forms.Select(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-3'})
    )
    Teams = forms.ModelChoiceField(
        queryset=Teams.objects.all(),
        label="Team",
        widget=forms.Select(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-3'})
    )
    class Meta:
        model = Task
        fields = ['Name', 'Description', 'Due_Date', 'Teams', 'AssignedUser']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-3'}),
            'Description': forms.Textarea(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-3', 'rows': 3}),
            'Due_Date': forms.DateInput(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-3', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # סינון ראשוני: רק משתמשים שיש להם פרופיל והם לא אדמינים
        self.fields['AssignedUser'].queryset = User.objects.filter(profile__role='EMPLOYEE')
    def clean(self):
        cleaned_data = super().clean()
        team = cleaned_data.get("Teams")
        user = cleaned_data.get("AssignedUser")
        if team and user:
            # בדיקה האם העובד שנבחר באמת שייך לצוות שנבחר
            if user.profile.team != team:
                raise forms.ValidationError("העובד שנבחר אינו משויך לצוות שנבחר!")
        return cleaned_data

    def clean_Due_Date(self):
        due_date = self.cleaned_data.get('Due_Date')
        if due_date and due_date < timezone.now().date():
            raise ValidationError("לא ניתן לקבוע משימה לתאריך שעבר!")
        return due_date

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']
        labels = {
            'team': 'Choose your team',
            'role': 'What is your role in the system?',
        }
        widgets = {
            'team': forms.Select(attrs={
                'class': 'bg-slate-800 border border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 transition-all outline-none appearance-none'
            }),
            'role': forms.Select(attrs={
                'class': 'bg-slate-800 border border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 transition-all outline-none appearance-none'
            }),
        }

