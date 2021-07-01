from django import forms
import datetime
from studentinfo.models import StudentBasicInfo,Address,AcademicInformation


def get_session():
    years = []
    for year in range(2016, (datetime.datetime.now().year+1)):
        years.append((str(year)+'-'+str(year+1),str(year)+'-'+str(year+1)))
    return years

class SBasicInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SBasicInfo, self).__init__(*args, **kwargs)
        self.fields['session'] = forms.ChoiceField(choices=get_session(),widget =forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = StudentBasicInfo
        fields = ['department_name','class_roll','semester','blod_group','photo','session']
        widgets = {
            'department_name': forms.Select(attrs={'class':'form-control'}),
            'semester': forms.Select(attrs={'class':'form-control'}),
            'class_roll': forms.NumberInput(attrs={'class':'form-control'}),
            'blod_group': forms.Select(attrs={'class':'form-control'}),
            #'email': forms.EmailInput(attrs={'class':'form-control'}),displayBlock=target
            'photo':forms.FileInput(attrs={'displayBlock':'target','type': 'file'})
            }


class CurrentAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields=['vill','city','dist','state','pin']
        widgets = {
            'vill': forms.TextInput(attrs={'class':'form-control','id':'CAVill'}),
            'city': forms.TextInput(attrs={'class':'form-control','id':'CAcity'}),
            'dist': forms.TextInput(attrs={'class':'form-control','id':'CAdist'}),
            'state': forms.TextInput(attrs={'class':'form-control','id':'CAstate'}),
            'pin': forms.NumberInput(attrs={'class':'form-control','id':'CApin'})
            }
        

class PermanentAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields=['vill','city','dist','state','pin']
        widgets = {
            'vill': forms.TextInput(attrs={'class':'form-control','id':'PAVill'}),
            'city': forms.TextInput(attrs={'class':'form-control','id':'PAcity'}),
            'dist': forms.TextInput(attrs={'class':'form-control','id':'PAdist'}),
            'state': forms.TextInput(attrs={'class':'form-control','id':'PAstate'}),
            'pin': forms.NumberInput(attrs={'class':'form-control','id':'PApin'})
            }

def get_years():
    years = []
    for year in range(1995, (datetime.datetime.now().year)):
       years.append((year,year))
    return years

class AcademicInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AcademicInfo, self).__init__(*args, **kwargs)
        self.fields['passing_year'] = forms.ChoiceField(choices=get_years(),widget =forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model=AcademicInformation
        fields=['degree','university_name','collage_name','Percentage','passing_year']
        widgets = {
            'degree': forms.TextInput(attrs={'class':'form-control','value':'Graduation'}),
            'university_name': forms.TextInput(attrs={'class':'form-control'}),
            'collage_name': forms.TextInput(attrs={'class':'form-control'}),
            'Percentage': forms.NumberInput(attrs={'class':'form-control'}),
            }
