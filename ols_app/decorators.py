from functools import wraps
from django.shortcuts import redirect

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Assuming 'role' is a field in your user model
        if request.user.is_authenticated and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('ols_name:dashboard')  # Redirect to a page that indicates access denied
    return _wrapped_view



def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Assuming 'role' is a field in your user model
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('ols_name:teacher_dashboard')  # Redirect to a page that indicates access denied
    return _wrapped_view