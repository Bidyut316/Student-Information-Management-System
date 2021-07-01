from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .forms import SBasicInfo,CurrentAddress,PermanentAddress,AcademicInfo
from .models import StudentBasicInfo,department_list,Address,AcademicInformation
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/login')
def student_info(request):
    if request.method=='GET':
        exist = True
        try:
            obj=StudentBasicInfo.objects.get(student=request.user.id)
        except StudentBasicInfo.DoesNotExist:
            exist=False
        print(exist)
        #print(request.user.id)
        if exist:
            print(obj.view_lock)
            return HttpResponseRedirect(reverse('department:verifi',kwargs={'slug': obj.slug}))
        context={
            'SBasicInfo':SBasicInfo,
            'Caddress':CurrentAddress,
            'Paddress':PermanentAddress,
            'AInfo':AcademicInfo,
            'exist':exist
        }
        return render(request, "SInfoForm.html",context)
    elif request.method=='POST':
        if request.user.is_authenticated: # +check user is student or not
            SBasic=SBasicInfo(request.POST,request.FILES)
            Caddress=CurrentAddress(request.POST)
            Paddress=PermanentAddress(request.POST)
            AInfo=AcademicInfo(request.POST)
            
            if SBasic.is_valid() and Caddress.is_valid() and Paddress.is_valid() and AInfo.is_valid():
                #SBasic.save()
                print(request.FILES.get('photo'))
                print('before commit')
                s_obj=SBasic.save(commit=False)
                
                s_obj.student=request.user
                s_obj.data_status='not verify'
                s_obj.student_status='current student'
                #print(request.user)
                print(request.FILES.get('photo'))
                print('before')
                s_obj.save()
                print(request.FILES.get('photo'))
                print('hoto')                #Caddress.save()
                c_obj=Caddress.save(commit=False)
                c_obj.student=request.user
                c_obj.address_type='Current Address'
                c_obj.save()
                
                #Paddress.save()
                p_obj=Paddress.save(commit=False)
                p_obj.student=request.user
                p_obj.address_type='Permanent Address'
                p_obj.save()
                #AInfo.save()
                a_obj=AInfo.save(commit=False)
                a_obj.student=request.user
                a_obj.save()
                return HttpResponse("Form valid ")
            else:
                return HttpResponse("Form not valid ")
