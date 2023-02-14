from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

# only allow logged in users to view this page
@login_required(login_url='login')
def coreapp(request):
    basket = 12

    context = {
        'basket' : basket
    }
    return render(request, 'coreapp/dashboard.html', context)
