from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def department_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.user_type.is_department == True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("accounts:home")
    return wrapper_function

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.user_type.is_admin == True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("accounts:home")
    return wrapper_function

def admin_or_department(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.user_type.is_admin == True or request.user.user_type.is_department == True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("accounts:home")
    return wrapper_function
