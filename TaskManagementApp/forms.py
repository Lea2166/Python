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

