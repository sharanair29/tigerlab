from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import FileForm


# only allow logged in users to view this page
@login_required(login_url='login')
def coreapp(request):
    files = Files.objects.filter(user=request.user)
    basket = TeamScore.objects.filter(user__username=request.user.username)
    context = {
        'basket' : basket,
        'files' : files
    }
    return render(request, 'coreapp/dashboard.html', context)

@login_required(login_url='login')
def deleteobj(request, pk):
        teamscore = TeamScore.objects.filter(pk=pk)
        teamscore.delete()
        return redirect('coreapp')

@login_required(login_url='login')
def deletefile(request, pk):
        files = Files.objects.filter(pk=pk)
        files.delete()
        return redirect('coreapp')

@login_required(login_url='login')
def analytics(request):
    teamscore = TeamScore.objects.filter(user__username=request.user.username)
    

    context = {

    }
    return render(request, 'coreapp/analytics.html', context)
