# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import *
# Create your views here.
def home_page(request):
    regform = Regform()
    loginform = Loginform()
    return render(request, "log_reg/index.html",{'regform':regform,'loginform':Loginform})
