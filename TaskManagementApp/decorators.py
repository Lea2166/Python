from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user.profile, 'role', None) == 'ADMIN':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "גישה זו מורשית למנהלים בלבד!")
            return redirect('alltasks') # הפניה לדף המשימות הרגיל
    return _wrapped_view