from django.db import models

# Create your models here.
from accounts.models import MyUser
import os
import random
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
user = get_user_model()
        #   File upload #
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    a=str(instance.student)
    user_folder=a.replace('@','_').replace('.','_')
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "{user}/Profile/{new_filename}/{final_filename}".format(
            user=user_folder,
            new_filename=new_filename, 
            final_filename=final_filename
            )

        #   End File upload #


class department_list(models.Model):
    d_name    =models.CharField(max_length=50,blank=False)

    def __str__(self):
        return self.d_name


class StudentBasicInfo(models.Model):
    data_status=(('verify','verify'),('not verify','not verify'))
    s_status=(('current student','current student'),('old student','old student'))
    semester_c=(('1st','1st'),('2nd','2nd'),('3rd','3rd'),('4th','4th'),('5th','5th'),('6th','6th'))
    blod_type=(('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-'))
        
    student     =models.OneToOneField(MyUser,on_delete=models.CASCADE)
    department_name =models.ForeignKey(department_list,on_delete=models.CASCADE,blank=True,null=True)
    class_roll      =models.SmallIntegerField(blank=False)
    semester        =models.CharField(max_length=10,choices=semester_c)
    blod_group      =models.CharField(max_length=10,choices=blod_type)
    session         =models.CharField(max_length=50,blank=True)
    photo           =models.ImageField(upload_to=upload_image_path,null=True, blank=False)

    
    slug            = models.SlugField(max_length=250,unique=True,blank=True)
    data_status     =models.CharField(max_length=50,choices=data_status,blank=False)
    student_status  =models.CharField(max_length=50,choices=s_status,blank=False)
    view_lock       =models.BooleanField(default=True)

    def __str__(self):
        return self.student.full_name + " - BasicInfo"

class Address(models.Model):
    addr_choices=(('Current Address','Current Address'),('Permanent Address','Permanent Address'))
    student     =models.ForeignKey(MyUser,on_delete=models.CASCADE)
    vill    =models.CharField(max_length=50,blank=True)
    city    =models.CharField(max_length=50,blank=True)
    dist    =models.CharField(max_length=50,blank=False)
    state   =models.CharField(max_length=50,blank=False)
    pin     =models.CharField(max_length=10,blank=False)
    address_type    =models.CharField(max_length=50,choices=addr_choices,default=None)

    def __str__(self):
        return self.student.full_name + "_" + self.address_type

class AcademicInformation(models.Model):
    student         =models.ForeignKey(MyUser,on_delete=models.CASCADE)
    degree          =models.CharField(max_length=50,blank=True)
    university_name =models.CharField(max_length=50,blank=True)
    collage_name    =models.CharField(max_length=50,blank=True)
    passing_year    =models.PositiveSmallIntegerField(blank=False)
    Percentage      =models.FloatField(max_length=50,blank=True)

    def __str__(self):
        return self.student.full_name + "_" + self.degree



def pre_save_unique_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_unique_slug, sender=StudentBasicInfo)
