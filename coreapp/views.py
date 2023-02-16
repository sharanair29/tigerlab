from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import FileForm
from django.db.models import Max, Subquery

#Custom sort dictionary function
def sort_dict_by_value(d, reverse = False):
  return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))

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
    """Get unique team names"""
    teamnames =  list(TeamScore.objects.filter(user=request.user).values_list('team_name_1', flat=True).distinct('team_name_1'))
    teamnames2 =  list(TeamScore.objects.filter(user=request.user).values_list('team_name_2', flat=True).distinct('team_name_2'))
    teams = teamnames + teamnames2
    """Assign 0 points to each team with team name as key in dictionary"""
    points = [0] * len(teams)
    team_points = dict(zip(teams, points))
    """Get all TeamScore uploaded values for the current user"""
    teamscore = TeamScore.objects.filter(user__username=request.user.username)
    """Loop through list of distinct team names and filter TeamScores by team name 1"""
    for t in teams:
        getValues = teamscore.filter(team_name_1 = f"{t}")
        for i in getValues:
            if i.team_score_1 == i.team_score_2:
                t1points = 1
                t2points = 1
            elif i.team_score_1 > i.team_score_2:
                t1points = 3
                t2points = 0
            else:
                t1points = 0
                t2points = 3
            """Update dictionary points per team looped"""
            teamname1 = team_points.get(t) + t1points
            teamname2 = team_points.get(i.team_name_2) + t2points
            team_points[f"{t}"] = teamname1
            team_points[f"{i.team_name_2}"] = teamname2
    """Sort dictionary in descending points value with custom function"""
    sorted_team_points = sort_dict_by_value(team_points, True)
    context = {
        'team_points' : sorted_team_points
    }
    return render(request, 'coreapp/analytics.html', context)
