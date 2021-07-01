from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login,get_user_model
from .models import user_type
from studentinfo.models import department_list
from django.urls import reverse
# Create your views here.
from .DepartmentList import t
from django.contrib.auth import logout
from django.contrib import messages
from DepartmentTask.decorators import unauthenticated_user
a=list(t)

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type.is_student:
             return render(request,'StudentHome.html',{'page':'student'})
        elif request.user.user_type.is_department:
            return HttpResponseRedirect(reverse('department:dhome'))
        else:
            return redirect("ATask:ahome")
    else:
        return render(request,'home.html',{'page':'home'})

def logout_view(request):
    logout(request)
    return redirect('accounts:home')

User = get_user_model()
@unauthenticated_user
def StudentRegistration(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save_stu()
        return redirect('accounts:login')
    return render(request, "Student_reg.html", context)

def DepartmentRegistration(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save_dep()
        x=form.cleaned_data.get('full_name')
        obj=department_list.objects.create(d_name=x)
        obj.save()
        return render(request,'AdminABody.html')
    return render(request,"DepartmrntReg.html", context)

@unauthenticated_user
def login2(request):
    context={
        'loginform':LoginForm
        }
    if (request.method == 'POST'):
        email = request.POST.get('email') #Get email value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            type_obj = user_type.objects.get(user=user)
            if user.is_authenticated and type_obj.is_student:
                return redirect("accounts:home") #Go to student home
            elif user.is_authenticated and type_obj.is_department:
                return HttpResponseRedirect(reverse('department:dhome')) #Go to department home
            elif user.is_authenticated and type_obj.is_admin:
                return redirect("ATask:ahome") #Go to admin home
        else:
            messages.error(request,'Username or Password not correct')
            # Invalid email or password. Handle as you wish
            return render(request,'login.html',context)

    return render(request, 'login.html',context)
