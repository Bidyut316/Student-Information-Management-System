from .import views
from django.urls import path,re_path
from django.urls import re_path

#from .views import RegisterView

app_name='DepartmentTask'
urlpatterns = [
    path('',views.DepartmentHome, name='dhome'),
    path('pending-record',views.PendingRecord, name='PRecord'),
    path('verifyed-record',views.VerifyedRecord, name='VRecord'),
    path('old-record',views.OldRecords, name='ORecord'),
    path('verifi/<slug:slug>',views.ShowStudentForVerifi,name='verifi'),
    path('cnfverify/<slug:slug>',views.cnfverify,name='cnfverify'),
    path('change-sem/<slug:slug>',views.change_sem,name='change_sem'),
    path('lock-unlock/<slug:slug>',views.lock_unlock,name='lock_unlock'),
    re_path(r'download-records/(?P<dep>\w+)?/(?P<sem>\w+)?/(?P<old_2>\w+)?/(?P<verify>\w+)?/(?P<roll>\w+)?$',views.download_records,name='DownloadRecords')
    #re_path(r'download-records/(?P<sem>\w+)?$',views.download_records,name='DownloadRecords')


]
