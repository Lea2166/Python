from django import forms
from .models import Task, Teams, Profile
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['Name', 'Description', 'Due_Date']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 outline-none'}),
            'Description': forms.Textarea(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 outline-none', 'rows': 3}),
            # הגדרת לוח השנה
            'Due_Date': forms.DateInput(attrs={
                'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 outline-none custom-calendar',
                'type': 'date'
            }),
        }
class AdminTaskForm(forms.ModelForm):
    # הוספת שדות בחירה עם עיצוב כהה
    AssignedUser = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="שייך לעובד",
        widget=forms.Select(attrs={'class': 'bg-slate-800 border-slate-700 text-white rounded-xl w-full p-3'})
    )
    Teams = forms.ModelChoiceField(
        queryset=Teams.objects.all(),
        label="צוות",
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

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']
        labels = {
            'team': 'בחר את הצוות שלך',
            'role': 'מה התפקיד שלך במערכת?',
        }
        widgets = {
            # עיצוב רשימת הבחירה של הצוותים
            'team': forms.Select(attrs={
                'class': 'bg-slate-800 border border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 transition-all outline-none appearance-none'
            }),
            # עיצוב רשימת הבחירה של התפקידים
            'role': forms.Select(attrs={
                'class': 'bg-slate-800 border border-slate-700 text-white rounded-xl w-full p-4 focus:ring-2 focus:ring-purple-500 transition-all outline-none appearance-none'
            }),
        }

