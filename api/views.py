from django.shortcuts import render, redirect
from coreapp.models import *
from coreapp.forms import FileForm
from django.http import HttpResponse
from rest_framework.response import Response
import io, csv

from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
#Serialize for data
class TeamScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamScore
        fields = "__all__"

class RankViewSet(viewsets.ModelViewSet):
    queryset = TeamScore.objects.all()
    serializer_class = TeamScoreSerializer
    @action(detail=False, methods=['POST'])
    def uploadfile(self,request):
        file = request.FILES.get("test")
        paramFile = io.TextIOWrapper(file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        create = Files.objects.create(user=request.user, file_uploaded=file)
        create.save()
        id = create.id
        getFile = Files.objects.get(pk=id)
        objs = [
                TeamScore(
                user = request.user,
                file = getFile,
                team_name_1 = row["team_1 name"],
                team_score_1 = row["team_1 score"],
                team_name_2 = row["team_2 name"],
                team_score_2 = row["team_2 score"],
                    
                )
                for row in list_of_dict
            ]
        print("posting works")
        msg = TeamScore.objects.bulk_create(objs)
        return redirect('coreapp')
       