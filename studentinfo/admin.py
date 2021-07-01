from django.contrib import admin
from .models import StudentBasicInfo,Address,AcademicInformation
# Register your models here.
admin.site.register(StudentBasicInfo)
admin.site.register(Address)
admin.site.register(AcademicInformation)
