from django import forms
from django.contrib.auth.models import User
from .models import *
import datetime
import base64
import re
import bcrypt
password_regex = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d).+$')
class UserProfileform(forms.ModelForm):
    years = [x for x in range(1949, 2011)]
    birthdate = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years = years))
    class Meta:
        model = UserProfile
        fields = ['birthdate',]
    def clean(self):
            birthdate = self.cleaned_data['birthdate']

class Regform(forms.ModelForm):
    confirm_password = forms.CharField(max_length=50, widget = forms.PasswordInput)
    username = forms.CharField(label="Email")
    class Meta:
        model = User
        fields=['first_name','last_name','username','password']
        widgets = {
            'password':forms.PasswordInput(),
            'email':forms.EmailInput(),
        }
    def clean(self):
        cleaned_data = super(Regform,self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.filter(email = email)
        print email
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
    username = forms.CharField(label="Email")
    password = forms.CharField(max_length=50, widget = forms.PasswordInput)
    def clean(self):
        email = self.cleaned_data.get('username')
        in_password = self.cleaned_data.get('password')
        login_users = User.objects.filter(username = email)
        if len(login_users) == 0 :
            raise forms.ValidationError("User does not exit !")

        else:
            password = User.objects.filter(username = email)[0].password
            if not bcrypt.checkpw(in_password.encode(),password.encode()):
                raise forms.ValidationError("Wrong password !")

class Invenform(forms.ModelForm):
    name = forms.CharField(min_length = 5)
    years = [x for x in range(1879, 2011)]
    # mfg_date = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years = years))
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
            ('20','20 liters pail'),
        )
        widgets = {
            #'location' : forms.Select(choices = location_choices),
            'container': forms.Select(choices = container_choices)
        }
class Profileform(forms.ModelForm):
    old_password = forms.CharField(widget = forms.PasswordInput)
    new_password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']
    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        old_password = self.cleaned_data.get('old_password') # input old password
        new_password = self.cleaned_data.get('new_password')
        user = User.objects.filter(email = email)
        password = user[0].password
        if "@raasnutritionals" not in email:
            raise forms.ValidationError("Please register with RAAS email")
        if len(user) > 1:
            raise forms.ValidationError("User already exists")
        if len(old_password) < 8 or len(new_password) < 8:
            raise forms.ValidationError('Password should be at least 8 characters')
        elif not  password_regex.match(new_password):
            raise forms.ValidationError('Password should at least have one letter')
        elif not bcrypt.checkpw(old_password.encode(),password.encode()):
            raise forms.ValidationError('Old password does not match !')
