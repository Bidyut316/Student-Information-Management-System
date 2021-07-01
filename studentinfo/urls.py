from .import views
from django.urls import path,re_path
#from .views import RegisterView

app_name='studentinfo'
urlpatterns = [
    path('',views.student_info, name='studentinfo'),
    

]
