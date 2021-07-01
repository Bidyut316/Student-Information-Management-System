import django_filters
from django_filters import DateFilter, CharFilter
from django.db import models
from django import forms
from studentinfo.models import StudentBasicInfo
from .models import DeleteRecords

import datetime
def get_session():
    years = []
    for year in range(2016, (datetime.datetime.now().year+1)):
        years.append((str(year)+'-'+str(year+1),str(year)+'-'+str(year+1)))
    return years


class RecordFilter(django_filters.FilterSet):
    
    #session = forms.ChoiceField(choices=get_session(),widget =forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = StudentBasicInfo
        fields = ['session','department_name','semester']
        filter_overrides = {
              models.CharField: {
                 'filter_class': django_filters.ChoiceFilter,
                 'extra': lambda f: {
                     'choices':get_session(),
                     'widget':forms.Select(attrs={'class':'form-control'}) 
                 },
             },
         }
        
class DeleteFilter(django_filters.FilterSet):
    name=CharFilter(field_name='name',lookup_expr='icontains')
    

