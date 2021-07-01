from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from studentinfo.models import StudentBasicInfo,department_list,Address,AcademicInformation
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from studentinfo .forms import SBasicInfo,CurrentAddress,PermanentAddress,AcademicInfo
from django.urls import reverse
from .filters import RecordFilter
from django.template.loader import render_to_string
import weasyprint
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .decorators import department_only,admin_or_department
# Create your views here.

@login_required(login_url='/login')
@department_only
def DepartmentHome(request):
    print(request.user.full_name)
    dname_obj=department_list.objects.get(d_name=request.user.full_name)
    obj=StudentBasicInfo.objects.filter(Q(department_name=dname_obj.id)&Q(data_status='not verify'))
    obj2=StudentBasicInfo.objects.filter(Q(department_name=dname_obj.id)&Q(data_status='verify')&Q(student_status='current student'))
    obj3=StudentBasicInfo.objects.filter(Q(department_name=dname_obj.id)&Q(data_status='verify')&Q(student_status='old student'))
    pending=obj.count()
    verifi=obj2.count()
    old=obj3.count()
    context={
        'pending':pending,
        'verifi':verifi,
        'old':old
        }
    return render(request,'AdminDBody.html',context)

@login_required(login_url='/login')
@department_only
def PendingRecord(request):
    dname_obj=department_list.objects.get(d_name=request.user.full_name)
    obj=StudentBasicInfo.objects.filter(Q(department_name=dname_obj.id)&Q(data_status='not verify'))


    
    myFilter = RecordFilter(request.GET, queryset=obj)
    obj = myFilter.qs
    #user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(obj, 2)
    print("Akash")
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request,'table.html',{'department_id':dname_obj.id,'records': records,'paginator':paginator,'myFilter':myFilter,'old':False,'dataverify':False })

@login_required(login_url='/login')
@department_only
def VerifyedRecord(request):
    dname_obj=department_list.objects.get(d_name=request.user.full_name)
    obj=StudentBasicInfo.objects.filter(Q(department_name=dname_obj.id)&Q(data_status='verify')&Q(student_status='current student'))
                                            #for Search element by Model fields
    myFilter = RecordFilter(request.GET, queryset=obj)
    obj = myFilter.qs
    #user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(obj, 1)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request,'table.html',{'department_id':dname_obj.id,'records': records,'paginator':paginator,'myFilter':myFilter,'old':False,'dataverify':True })

@login_required(login_url='/login')
@department_only
def OldRecords(request):
    dname_obj=department_list.objects.get(d_name=request.user.full_name)
    obj=StudentBasicInfo.objects.filter(Q(department_name=dname_obj.id)&Q(data_status='verify')&Q(student_status='old student'))
                                            #for Search element by Model fields
    myFilter = RecordFilter(request.GET, queryset=obj)
    obj = myFilter.qs
    #user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(obj, 1)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request,'table.html',{'department_id':dname_obj.id,'records': records,'paginator':paginator,'myFilter':myFilter,'old':True,'dataverify':True })

@login_required(login_url='/login')

def ShowStudentForVerifi(request,slug):
    obj=StudentBasicInfo.objects.get(slug = slug)
    #SBasicInfo2 = SBasicInfo(request.POST or None, instance = obj) 
    SBasicInfo2 = SBasicInfo(instance=obj)#1
    SBasicInfo2.fields['photo'].required = False
    c_obj=Address.objects.filter(student=obj.student)
    ca_obj=c_obj.get(address_type='Current Address')
    pa_obj=c_obj.get(address_type='Permanent Address')
    CurrentAddress2=CurrentAddress(instance=ca_obj)#2
    PermanentAddress2=PermanentAddress(instance=pa_obj)#3
    AcademicInfo2=AcademicInfo(instance=AcademicInformation.objects.get(student=obj.student))#4
    img=obj.photo
    context={
            'SBasicInfo':SBasicInfo2,
            'Caddress':CurrentAddress2,
            'Paddress':PermanentAddress2,
            'AInfo':AcademicInfo2,
            'obj':obj,
           
        }
    if request.method=='POST':
        if obj.view_lock  and request.user.user_type.is_student:
            return HttpResponseRedirect(reverse('department:verifi',kwargs={'slug': slug}))
        else:
            SB= SBasicInfo(request.POST,request.FILES,instance=obj)
            if obj.view_lock == False  and request.user.user_type.is_student:
                sb_obj=SB.save(commit=False)
                sb_obj.view_lock = True
                sb_obj.save()
            else:
                SB.save()
            CA= CurrentAddress(request.POST,instance=ca_obj)
            CA.save()
           
            #PA= PermanentAddress(request.POST,request.FILES,instance=pa_obj)
            #PA.save()
            
            AI= AcademicInfo(request.POST,request.FILES,instance=AcademicInformation.objects.get(student=obj.student))
            AI.save()                
        return HttpResponseRedirect(reverse('department:verifi',kwargs={'slug': slug}))
    return render(request,'StudentFormForVerifi.html',context)

@login_required(login_url='/login')
@department_only
def cnfverify(request,slug):
    SB= SBasicInfo(instance=StudentBasicInfo.objects.get(slug = slug))
    SB_obj=SB.save(commit=False)
    SB_obj.data_status='verify'
    print('verify')
    SB_obj.save()
    return HttpResponseRedirect(reverse('department:verifi',kwargs={'slug': slug}))

@login_required(login_url='/login')
@admin_or_department
def download_records(request,dep=None,sem=None,roll=None,old_2=None,verify=None):
    print(verify)
    if old_2 == 'True':
        obj=StudentBasicInfo.objects.filter(Q(data_status='verify')&Q(student_status='old student'))
        if dep != 'None' and dep != None:
            obj=obj.filter(department_name=dep)
    else:
        obj=StudentBasicInfo.objects.filter(student_status='current student')
        if verify == 'True':
            obj=obj.filter(data_status='verify')
        else:
           obj=obj.filter(data_status='not verify')
        if dep != 'None' and dep != None:
            obj=obj.filter(department_name=dep)
        if sem != 'None' and sem != None:
            obj=obj.filter(semester=sem)
        if roll != 'None' and roll != None:
            obj=obj.filter(class_roll=roll)
    #dname_obj=department_list.objects.get(d_name=request.user.full_name)
    #obj=StudentBasicInfo.objects.filter(Q(department_name=dname_obj.id)&Q(data_status='verify'))
    #obj=StudentBasicInfo.objects.all()
    
    html = render_to_string('DownloadRecords.html',{'obj':obj})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"ssdd.pdf"'
    weasyprint.HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(response,presentational_hints=True)
    return response

@login_required(login_url='/login')
@department_only
def change_sem(request,slug):
    dic={'1st':'2nd','2nd':'3rd','3rd':'4th','4th':'5th','5th':'6th'}
    obj=StudentBasicInfo.objects.get(slug=slug)
    sem=request.GET['sem']
    print('ajax .......')
    print(obj.semester)
    basicform=SBasicInfo(instance=obj)
    ss=basicform.save(commit=False)
    if sem in dic.keys():
        ss.semester=dic[sem]
        passout=False
    elif sem == '6th':
        ss.student_status='old student'
        passout = True
    ss.save()
    print(request.GET['sem'])
    #print(basicform)
    data = dict()
    #print(obj.semester)
    context = {'object': obj,'passout':passout}
    data['html_td'] = render_to_string('ajax_pass.html',
        context,
        request=request
    )
    return JsonResponse(data)

@login_required(login_url='/login')
@admin_or_department
def lock_unlock(request,slug):
    lockdata= dict()
    obj_st=StudentBasicInfo.objects.get(slug=slug)
    basicform=SBasicInfo(instance=obj_st)
    if obj_st.view_lock:
        basic_obj=basicform.save(commit=False)
        basic_obj.view_lock = False
        basic_obj.save()
        lockdata['icon']='''<i class="fa fa-unlock fa-2x" aria-hidden="true" style="color:  #0099CC;"></i>'''
    else:
        basic_obj=basicform.save(commit=False)
        basic_obj.view_lock = True
        basic_obj.save()
        lockdata['icon']='''<i class="fa fa-lock fa-2x" aria-hidden="true" style="color:  #0099CC;"></i>'''  
    return JsonResponse(lockdata)
