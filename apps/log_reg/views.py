# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from datetime import datetime
from django.shortcuts import render,redirect,HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
import json
# #####################################
# page load function below
##########################################
def home_page(request):
    regform = Regform()
    loginform = Loginform()
    profile_form = UserProfileform()
    return render(request, "log_reg/index.html",{'regform':regform,'loginform':Loginform, 'profile_form':profile_form})

def logout(request):
    auth_logout(request)
    return redirect ('/')


@login_required(login_url='/')
def inventory(request,id):
    invens = Inventory.objects.all()
    log_user = User.objects.filter(id = id)[0]
    print log_user.userprofile.level
    context = {
        'log_user':log_user,
        'invens':invens
    }
    return render(request, 'log_reg/inventory.html',context)
@login_required(login_url='/')
def update_page(request,id):
    update_form = Invenform()
    return render(request, 'log_reg/update.html',{'update_form':update_form,'log_user':User.objects.filter(id = request.session['log_id'])[0]})
@login_required(login_url='/')
def profile(request,id):
    log_user = User.objects.filter(id = id)[0]
    profile_form = Profileform()
    return render(request, 'log_reg/profile.html',{'log_user':log_user, 'profile_form':profile_form})
@login_required(login_url="/")
def location(request,location):
    products = Inventory.objects.filter(location = location)
    return render(request, 'log_reg/location.html', {'products':products, "location":location, 'log_id':request.session['log_id'],'log_name':request.session['log_name']})

@login_required(login_url="/")
def pname(request,pname): # sort product by product name (pname)
    products = Inventory.objects.filter(name = pname).order_by("lot_num")

    context={
        "products":products,
        "name":pname,
        "log_id":request.session["log_id"],
        "log_name":request.session["log_name"],

    }
    return render(request, "log_reg/pname.html",context)
##############################################
#   process handle function below:
#################################################

def register(request):
    bound_form = Regform(request.POST)
    bound_form2 = UserProfileform(request.POST)
    if bound_form.is_valid() and bound_form2.is_valid():
        reg_user = bound_form.save(commit=False)# created an instance(instantiate) but no save into database
        password = bound_form.cleaned_data['password'];
        reg_user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(15))
        reg_user.save() # models.py line 15, when User saves, then an instance of UserProfile will be created
        birthdate = bound_form2.cleaned_data['birthdate']
        reg_user.userprofile.birthdate = birthdate  # reg_user is an instance of User, and User has OneToOne relationship with UserProfile with related_name "userprofile"
        reg_user.userprofile.save()#
        messages.success(request,"Registered successfully!")
    else:
        return render(request, 'log_reg/index.html',{'loginform':Loginform(),'regform':bound_form,'profile_form':UserProfileform()})
    return redirect('/')
def login(request):
    bound_form = Loginform(request.POST)
    if bound_form.is_valid():
        password =  bound_form.cleaned_data.get('password')
        username = bound_form.cleaned_data.get('username')
        user_id = User.objects.filter(username = username)[0].id
        user_name = User.objects.filter(username = username)[0].first_name
        request.session['log_id'] = user_id
        request.session['log_name'] = user_name
        user = authenticate(request, username = username, password = password) # customize authentication backend so that it is able to check hashed password
        if user is not None:
            print " user is not none"
            if user.is_active:
                auth_login(request,user)
                return redirect('inventory',id = request.session['log_id'])
    return render(request,"log_reg/index.html",{'regform':Regform(),'loginform':bound_form, 'profile_form':UserProfileform})

@login_required(login_url='/')
def update(request):
    bound_form = Invenform(request.POST)
    print bound_form.is_valid()
    if bound_form.is_valid():
        product = bound_form.save(commit=False)
        container = float(bound_form.cleaned_data.get('container'))
        net_quantity = bound_form.cleaned_data.get('net_quantity')
        pnet_quantity = bound_form.cleaned_data.get('pnet_quantity')
        tquantity = container*net_quantity+pnet_quantity
        product.tquantity = tquantity
        print product.mfg_date
        bound_form.save(commit=True)
        return redirect('inventory', id = request.session['log_id'])
    else:
        messages.error(request, 'Error')
        return redirect('update_page', id = request.session['log_id'])

@login_required(login_url='/')
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

@login_required(login_url='/')
def delete(request):
    prodid = request.POST.get("prodid")
    d = Inventory.objects.get(id = prodid)
    d.delete()
    return HttpResponse("delete succeed!")

@login_required(login_url='/')
def edit(request):
    data = []
    data = request.POST.get("data")
    data_list = json.loads(data) # make string back to list, also json.dumps() can be used to make list to string
    prodid = request.POST.get("prodid")
    e = Inventory.objects.get(id = prodid)
    print "quantity is" +str(data_list[2])
    e.location = data_list[0]
    e.container = data_list[1]
    e.net_quantity = int(data_list[2])
    e.pnet_quantity = float(data_list[3])
    e.tquantity = float(e.container)*e.net_quantity+e.pnet_quantity
    print "total quantity are" + str(e.tquantity)
    e.save()
    date_temp = datetime.datetime.strptime(data_list[5],"%m/%d/%Y").strftime("%Y-%m-%d")
    History.objects.create(product = Inventory.objects.get(id = prodid),actioner=data[4],location = data_list[0],container = data_list[1],net_quantity = int(data_list[2]),pnet_quantity = float(data_list[3]),date=date_temp)
    print date_temp
    return HttpResponse("saved change!")
@login_required(login_url='/')
def lot_num(request,lot_num):

    product = Inventory.objects.filter(lot_num = lot_num)[0]
    history = product.history.all()
    print "lot number is " +str(product.lot_num)
    action_form = Actionform()
    return render(request,"log_reg/lot_num.html",{'product' : product, 'action_form':action_form, 'history':history})


@login_required(login_url='/')
def action(request, lot_num):
    bound_form = Actionform(request.POST)
    product = Inventory.objects.filter(lot_num = lot_num)[0]
    history = product.history
    if bound_form.is_valid():

        container = product.container
        action = bound_form.save(commit=False)
        net = action.net_quantity
        partial = action.pnet_quantity
        action.tquantity = float(container)*net+partial
        action.actioner = User.objects.filter(id = request.session['log_id'])[0].id
        action.product_id = product.id
        bound_form.save(commit=True)
        ## update Inventory
        product.net_quantity += net
        product.pnet_quantity += partial
        product.tquantity += action.tquantity
        product.save()
        return redirect('lot_num', lot_num = lot_num)
    else:
        return render(request,"log_reg/lot_num.html",{'product' : product, 'action_form':bound_form,'history':history})
