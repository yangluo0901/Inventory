from django import forms
from .models import *
import datetime
class Regform(forms.ModelForm):
    years = [x for x in range(1879, 2011)]
    confirm_password = forms.CharField(max_length=50, widget = forms.PasswordInput)
    birthdate = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years = years))
    class Meta:
        model = User
        fields=['first_name','last_name','email','password','birthdate']
        widget = {
            'password':forms.PasswordInput(),
            'email':forms.EmailInput(),
        }
class Loginform(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=15,widget = forms.PasswordInput)
