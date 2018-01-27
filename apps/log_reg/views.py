# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
# Create your views here.
def home_page(request):
    regform = Regform()
    loginform = Loginform()
    return render(request, "log_reg/index.html",{'regform':regform,'loginform':Loginform})

def inventory(request,id):
    invens = Inventory.objects.all();

    log_user = User.objects.filter(id = id)

    context = {
        'log_user':log_user,
        'invens':invens
    }
    return render(request, 'log_reg/inventory.html',context)
def update_page(request,id):
    update_form = Invenform()
    return render(request, 'log_reg/update.html',{'update_form':update_form})

def register(request):
    bound_form = Regform(request.POST)
    if bound_form.is_valid():
        birthdate = bound_form.cleaned_data['birthdate']
        reg_user = bound_form.save(commit=False)
        reg_user.birthdate = birthdate
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
