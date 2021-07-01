from django import forms
from .models import DeleteRecords,Mails



class DeleteForm(forms.ModelForm):
    class Meta:
        model = DeleteRecords
        fields = ['reson']
        widgets = {
            'reson': forms.Textarea(attrs={'class':'form-control',"rows":5, "cols":10})
            }

class EmailForm(forms.ModelForm):
    attach = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'class':'form-controlj','multiple': True}))
    class Meta:
        model = Mails
        fields = ['email','subject','message']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control','type':'hidden'}),
            'subject':forms.TextInput(attrs={'class':'form-control'}),
            'message':forms.Textarea(attrs={'class':'form-control',"rows":5, "cols":10})
            }
    '''email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','type':'hidden'}))
    subject = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))
    attach = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'class':'form-controlj'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control',"rows":5, "cols":10}))'''
