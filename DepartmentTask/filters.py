import django_filters
from django_filters import DateFilter, CharFilter
from django.db import models
from django import forms
from studentinfo.models import StudentBasicInfo
import datetime
def get_session():
    years = []
    for year in range(2016, (datetime.datetime.now().year+1)):
        years.append((str(year)+'-'+str(year+1),str(year)+'-'+str(year+1)))
    return years


class RecordFilter(django_filters.FilterSet):
    class_roll = CharFilter(field_name='class_roll')
    class Meta:
        model = StudentBasicInfo
        fields=['semester','session']
        filter_overrides = {
              models.CharField: {
                 'filter_class': django_filters.ChoiceFilter,
                 'extra': lambda f: {
                     'choices':get_session(),
                     'widget':forms.Select(attrs={'class':'form-control'}) 
                 },
             },
         }
        
        '''start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	note = CharFilter(field_name='note', lookup_expr='icontains')'''
