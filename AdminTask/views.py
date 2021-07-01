from django.shortcuts import render,HttpResponse
from studentinfo.models import StudentBasicInfo
from accounts.models import MyUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import RecordFilter,DeleteFilter
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import DeleteForm,EmailForm
from django.shortcuts import redirect
from .models import DeleteRecords,Mails
# Create your views here.
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from DepartmentTask.decorators import admin_only,admin_or_department

import json

@login_required(login_url='/login')
@admin_only
def AdminHome(request):
    return render(request,'AdminABody.html')

@login_required(login_url='/login')
@admin_only
def Current_All_Student(request):
    obj=StudentBasicInfo.objects.filter(Q(student_status='current student')&Q(data_status='verify'))
    page = request.GET.get('page', 1)
    myFilter = RecordFilter(request.GET, queryset=obj)
    obj = myFilter.qs
    paginator = Paginator(obj, 5)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request,'table.html',{ 'records': records,'paginator':paginator,'myFilter':myFilter,'old':False,'dataverify':True })

@login_required(login_url='/login')
@admin_only
def Old_All_Student(request):
    obj=StudentBasicInfo.objects.filter(Q(student_status='old student')&Q(data_status='verify'))
    page = request.GET.get('page', 1)
    myFilter = RecordFilter(request.GET, queryset=obj)
    obj = myFilter.qs
    paginator = Paginator(obj, 1)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request,'table.html',{ 'records': records,'paginator':paginator,'myFilter':myFilter,'old':True,'dataverify':True })

def delete_form_load(request):
    data = dict()
    print("delete Ajax")
    context={
        'delete_form':DeleteForm,
        'slug':request.GET['sl'],
        'path':request.GET['pt']
        }
    data['html_form'] = render_to_string('delete_form.html',context,request=request)
    return JsonResponse(data)

@login_required(login_url='/login')
@admin_or_department
def delete_record(request,slug):
    pt=request.POST.get("path")
    obj=StudentBasicInfo.objects.get(slug=slug)
    df=DeleteForm(request.POST)
    if df.is_valid():
        delete_obj=MyUser.objects.get(email=obj.student.email)
        #delete_obj.delete()
        print(delete_obj)
        df_obj=df.save(commit=False)
        if request.user.user_type.is_department:
            df_obj.by_whom='Department Of '+ request.user.full_name
        else:
            df_obj.by_whom=request.user.full_name
            
        df_obj.delete_userid=obj.student.email
        df_obj.name=obj.student.full_name
        df_obj.session=obj.session
        if obj.data_status == 'verify':
            df_obj.data_status='Verifyed'
        else:
            df_obj.data_status='Not Verifyed'
        df_obj.save()
    print(request.path)
    response = redirect(pt)
    return response

@login_required(login_url='/login')
@admin_only
def show_deleted_records(request):
    obj=DeleteRecords.objects.all()
    myFilter = DeleteFilter(request.GET, queryset=obj)
    obj = myFilter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(obj, 5)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(request,'delete_table.html',{ 'records': records,'paginator':paginator,'myFilter':myFilter})

@login_required(login_url='/login')
@admin_or_department    
def load_mail_form(request):
    data = dict()
    print("email Ajax")
    #print(request.POST['objects'])
    #rec_data=json.loads(request.body)
    #rec2_data=json.dumps(rec_data)
    #print(type(rec_data))
    #print(type(rec2_data))
    
    #for i in rec_data:
     #   print(rec-data[i]['name'])
    if request.method=='GET':
        context={
        'mail_form':EmailForm,
        'email':request.GET['mail']
        }
    else:
        context={
        'mail_form':EmailForm,
        'email':'bidyutmandal316@gmail.com' # set value for form valid
        }
    data['html_form'] = render_to_string('email_form.html',context,request=request)
    return JsonResponse(data)

@login_required(login_url='/login')
@admin_or_department
def SendMail(request):
    return_data = dict()
    form = EmailForm(request.POST,request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form_obj=form.save(commit=False)
        form_obj.save()
        '''if len(request.FILES.getlist('attach')) !=0:
            for file in request.FILES.getlist('attach'):
                file_instance = Mails(document=file)
                file_instance.save()'''
        rec_data=request.POST.get('myData')
        print(type(rec_data))
        rec_data2=json.loads(rec_data)
        print(type(rec_data2))
        #email = form.cleaned_data.get('email')
        email='bidyutmandal316@gmail.com'
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        #print('Test doc',document)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        return_data['mail_is_send'] = True
        eml = EmailMessage(subject,message,email_from,recipient_list)
        base_dir = 'media/Maildocuments/'
        if len(request.FILES.getlist('attach')) !=0:
            doc =request.FILES.getlist('attach')
            for f in doc:
                eml.attach(f.name,f.read(),f.content_type)
                file_instance = Mails(document=f)
                file_instance.save()
            #document=str(doc).replace(' ','_')
            #print(document)
            #eml.attach_file('media/Maildocuments/'+document)
        eml.send()

        '''print(form.cleaned_data.get('email'))
        print(request.POST.get('email'))
        print(form.cleaned_data.get('attach'))'''
    return JsonResponse(return_data)
    
