from .import views
from django.urls import path,re_path
#from .views import RegisterView

app_name='accounts'
urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login2, name='login'),
    path('SReg/', views.StudentRegistration, name='SReg'),
    path('DReg/', views.DepartmentRegistration, name='DReg'),

]
