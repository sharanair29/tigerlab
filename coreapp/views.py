from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import FileForm
from django.db.models import Max, Subquery

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
    teamnames =  list(TeamScore.objects.filter(user=request.user).values_list('team_name_1', flat=True).distinct('team_name_1'))
    teamnames2 =  list(TeamScore.objects.filter(user=request.user).values_list('team_name_2', flat=True).distinct('team_name_2'))
    teams = teamnames + teamnames2
    # print(teams)
    points = [0] * len(teams)
    team_points = dict(zip(teams, points))
    print(team_points)
    teamscore = TeamScore.objects.filter(user__username=request.user.username)
    
    # for i in teamscore:
    #     if i.team_score_1 == i.team_score_2:
    #         t1points = 1
    #         t2points = 1
    #     else:
    #         if i.team_score_1 > i.team_score_2:
    #             t1points = 3
    #             t2points = 0
    #         else:
    #             t1points = 0
    #             t2points = 3
    # teamname1 = team_points.get(i.team_name_1) + t1points
    # teamname2 = team_points.get(i.team_name_2) + t2points
    # team_points[f"{i.team_name_1}"] = teamname1
    # team_points[f"{i.team_name_2}"] = teamname2
    # print(teamname1)
    # print(teamname2)
    
    context = {
        'team_points' : team_points
    }
    return render(request, 'coreapp/analytics.html', context)
