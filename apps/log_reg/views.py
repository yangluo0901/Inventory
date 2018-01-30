# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
# #####################################
# page load function below
##########################################
def home_page(request):
    regform = Regform()
    loginform = Loginform()
    profile_form = UserProfileform()
    return render(request, "log_reg/index.html",{'regform':regform,'loginform':Loginform, 'profile_form':profile_form})

def inventory(request,id):
    invens = Inventory.objects.all();

    log_user = User.objects.filter(id = id)[0]

    context = {
        'log_user':log_user,
        'invens':invens
    }
    return render(request, 'log_reg/inventory.html',context)
def update_page(request,id):
    update_form = Invenform()
    return render(request, 'log_reg/update.html',{'update_form':update_form})

def profile(request,id):
    log_user = User.objects.filter(id = id)[0]
    profile_form = Profileform()

    return render(request, 'log_reg/profile.html',{'log_user':log_user, 'profile_form':profile_form})

##############################################
#   process handle function below:
#################################################

def register(request):
    bound_form = Regform(request.POST,instance=request.user)
    bound_form2 = UserProfileform(request.POST,instance=request.user.userprofile)
    if bound_form.is_valid() and bound_form2.is_valid():
        birthdate = bound_form2.cleaned_data['birthdate']
        reg_user2 = bound_form2.save(commit=False)
        reg_user2.birthdate = birthdate
        reg_user = bound_form.save(commit=False)
        bound_form2.save(commit=True)

        password = bound_form.cleaned_data['password'];
        reg_user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(15))
        bound_form.save(commit=True)

        messages.success(request,"Registered successfully!")
    else:
        return render(request, 'log_reg/index.html',{'loginform':Loginform(),'regform':bound_form})
    return redirect('/')
def login(request):
    bound_form = Loginform(request.POST)
    if bound_form.is_valid():
        email =  bound_form.cleaned_data.get('email')
        user_id = User.objects.filter(email = email)[0].id
        request.session['log_id'] = user_id
        return redirect('inventory',id = request.session['log_id'])

    else:
        return render(request,"log_reg/index.html",{'regform':Regform(),'loginform':bound_form})
def update(request):
    bound_form = Invenform(request.POST)
    if bound_form.is_valid():
        product = bound_form.save(commit=False)
        container = float(bound_form.cleaned_data.get('container'))
        net_quantity = bound_form.cleaned_data.get('net_quantity')
        pnet_quantity = bound_form.cleaned_data.get('pnet_quantity')
        tquantity = container*net_quantity+pnet_quantity
        product.tquantity = tquantity
        bound_form.save(commit=True)
        return redirect('inventory', id = request.session['log_id'])
    else:
        messages.error(request, 'Error')
        return redirect('update_page', id = request.session['log_id'])

def profile_update(request, id):
    update_user = User.objects.filter(id = id)[0]
    bound_form = Profileform(request.POST, instance = update_user)

    if bound_form.is_valid():
        new_password = bound_form.cleaned_data.get('new_password')
        A = bound_form.save(commit=False)
        A.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(15))
        bound_form.save(commit = True)
        messages.success(request,'Profile updated !')
        return redirect('profile', id = request.session['log_id'])
    else:
        return render(request, 'log_reg/profile.html', {'profile_form':bound_form, 'log_user':log_user})
