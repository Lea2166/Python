from django import forms
from .models import Task, Teams
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['Name', 'Description', 'Due_Date']
        # ווידג'טים מעוצבים כפי שהיו

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