from .import views
from django.urls import path,re_path
#from .views import RegisterView

app_name='AdminTask'
urlpatterns = [
    path('',views.AdminHome, name='ahome'),
    path('current-record/',views.Current_All_Student, name='CAllStu'),
    path('old-record/',views.Old_All_Student, name='OAllStu'),
    path('delete-form/',views.delete_form_load, name='delete_form_ajax'),
    path('delete-record/<slug:slug>',views.delete_record, name='delete_record'),
    path('deleted-records_show/',views.show_deleted_records, name='show_deleted'),
    path('load-mail-form/',views.load_mail_form, name='load_mail_form'),
    path('sendmail/',views.SendMail, name='sendmail'),

]
