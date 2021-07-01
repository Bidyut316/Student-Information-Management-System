from django.db import models

# Create your models here.

class DeleteRecords(models.Model):
    by_whom     =models.CharField(max_length=100,blank=False)
    delete_date =models.DateTimeField(auto_now_add=True)
    reson       =models.TextField(blank=False)
    delete_userid   =models.CharField(max_length=100,blank=False)
    name        =models.CharField(max_length=50,null=True)
    session     =models.CharField(max_length=50,blank=True)
    data_status     =models.CharField(max_length=50,blank=False)

    def __str__(self):
        return self.delete_userid + " is deleted"

class Mails(models.Model):
    email =     models.EmailField() 
    subject =   models.CharField(max_length=1000)
    message = models.CharField(max_length=20000)
    document = models.FileField(upload_to='Maildocuments/')
    def __str__(self):
        return self.email  
