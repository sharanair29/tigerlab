from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import TeamScoreForm
import json 
from django.core.cache import cache
#Custom sort dictionary function
# If reverse is True sort by descending order of values
# If reverse is False sort by ascending order of values 
def sort_dict_by_value(d, reverse = False):
  return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))

# only allow logged in users to view this page
#view to upload csv files with team scores, delete files, delete individual team scores objects
@login_required(login_url='login')
def analytics(request):
    """filter all files uploaded by user to load team scores"""
    files = Files.objects.filter(user=request.user)
  
    """Add Team Score Form"""
    addform = TeamScoreForm()

    context = {

        'files' : files,
        'addform' : addform
    }
    return render(request, 'coreapp/analytics.html', context)

#delete team score object
@login_required(login_url='login')
def deleteobj(request, pk):
        """delete individual team score object generated from file upload"""
        teamscore = get_object_or_404(TeamScore, pk=pk)
        teamscore.delete()
        cache.clear()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "dataListChanged": None,
                    "showMessage": f"{teamscore.id} deleted."
                })
            })

#add team score object
@login_required(login_url='login')
def addobj(request):
        if request.method == 'POST':
            create = TeamScore.objects.create(user=request.user, file = None)
            create.save()
            id = create.id
            getts = TeamScore.objects.filter(pk=id).first()
            teamscore = TeamScoreForm(request.POST, request.FILES, instance=getts)
       
            if teamscore.is_valid:
                teamscore.save()
                cache.clear()
                return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "dataListChanged": None,
                        "showMessage": f"{getts.id} added."
                    })
                })
               
        else:
            form = TeamScoreForm()
        titlevalue = "Add Data"
        return render(request, 'coreapp/editdata.html', {
            'form': form,
            'titlevalue' : titlevalue
        })


@login_required(login_url='login')
def edit_data(request, pk):
    if cache.get(pk):
        ts = cache.get(pk)
        print("hit the cache")
    else:
        ts = get_object_or_404(TeamScore, pk=pk)
        cache.set(pk, ts)
        print("hit the db")
    if request.method == "POST":
        
        form = TeamScoreForm(request.POST, instance=ts)
        if form.is_valid():
            form.save()
            cache.clear()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "dataListChanged": None,
                        "showMessage": f"{ts.team_name_1} updated."
                    })
                }
            )
    else:
        form = TeamScoreForm(instance=ts)
    titlevalue = "Edit Data"
    return render(request, 'coreapp/editdata.html', {
        'form': form,
        'teamscore': ts,
        'titlevalue' : titlevalue
    })

#Get list of team score objects for the user
@login_required(login_url='login')
def listteamscores(request):
    """filter all team scores objects generated from uploaded files by user"""
    user = request.user.username
    if cache.get(user):
        print("hit the cache")
        basket = cache.get(user)
    else:
        basket = TeamScore.objects.filter(user__username=user)
        cache.set(
            user,
            basket
        )
        print("hit the db for list of team scores")

    context = {
        'basket' : basket
    }
    return render(request, 'coreapp/listteamscores.html', context)

#Delete file uplooad
@login_required(login_url='login')
def deletefile(request, pk):
        """delete file uploaded and linked team score objects from file upload"""
        files = Files.objects.filter(pk=pk)
        files.delete()
        cache.clear()
        return redirect('analytics')

#view to compute the rank and points of team scores
@login_required(login_url='login')
def coreapp(request):
    return render(request, 'coreapp/dashboard.html')


@login_required(login_url='login')
def ranks(request):
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
        'team_points' : sorted_team_points,
    }
    return render(request, 'coreapp/ranks.html', context)