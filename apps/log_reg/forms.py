from django import forms
from .models import *
import datetime
import base64
import re
import bcrypt
password_regex = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d).+$')
class Regform(forms.ModelForm):
    years = [x for x in range(1879, 2011)]
    confirm_password = forms.CharField(max_length=50, widget = forms.PasswordInput)
    birthdate = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years = years))
    class Meta:
        model = User
        fields=['first_name','last_name','email','password','birthdate']
        widgets = {
            'password':forms.PasswordInput(),
            'email':forms.EmailInput(),
        }
    def clean(self):
        cleaned_data = super(Regform,self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        user = User.objects.filter(email = email)
        if "@raasnutritionals" not in email:
            raise forms.ValidationError("Please register with RAAS email")
        if len(user) > 0:
            raise forms.ValidationError("User already exists")
        if len(password) < 8:
            raise forms.ValidationError('Password should be at least 8 characters')
        elif not password_regex.match(password):
            raise forms.ValidationError('Password should at least have one letter')
        elif confirm_password != password:
            raise forms.ValidationError('Password does not match !')
        return super(Regform,self).clean()



class Loginform(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget = forms.PasswordInput)
    def clean(self):
        email = self.cleaned_data.get('email')
        in_password = self.cleaned_data.get('password')
        print in_password
        login_users = User.objects.filter(email = email)
        if len(login_users) == 0 :
            raise forms.ValidationError("User does not exit !")

        else:
            password = User.objects.filter(email = email)[0].password
            if not bcrypt.checkpw(in_password.encode(),password.encode()):
                raise forms.ValidationError("Wrong password !")

class Invenform(forms.ModelForm):
    name = forms.CharField(min_length = 5)
    years = [x for x in range(1879, 2011)]
    #mfg_date = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years = years))
    mfg_date = forms.DateField(input_formats=["%m/%d/%Y"])
    location_choices = (
        ('LR-WC1','LR-WC1'),
        ('LR-WC2','LR-WC2'),
        ('PP-REFRIG1','PP-REFRIG1'),
        ('PP-REFRIG2','PP-REFRIG2'),
        ('PP-REFRIG3','PP-REFRIG3')
    )
    location = forms.ChoiceField(choices = location_choices)
    class Meta:
        model = Inventory
        fields = ['name','lot_num','location','container','net_quantity','pnet_quantity','mfg_date']

        container_choices = (
            ('0.74','740 ml bottle'),
            ('3.86','1 gallon jug'),
            ('20','20 liters pail')
        )
        widgets = {
            #'location' : forms.Select(choices = location_choices),
            'container': forms.Select(choices = container_choices)
        }
