from django.shortcuts import redirect
from coreapp.models import *
import io, csv, codecs
from django.contrib import messages
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
import traceback
import logging
from django.core.cache import cache
logging.basicConfig(filename="./log.txt", level=logging.DEBUG)


# Serialize for data
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
        try:
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
        
            msg = TeamScore.objects.bulk_create(objs)
            cache.clear()
            logging.info("Success no key error, " + f"Time : {timezone.now()}")
            print("posting works")
            return redirect('coreapp')
        except KeyError as e:
            try:
                print(traceback.format_exc())
                logging.info("Success key fall back, " + f"Time : {timezone.now()}")
                reader = csv.reader(open(getFile.file_uploaded.path,'r',  encoding='utf-8'))
                listtest = list(reader)
                headers = listtest.pop(0)
                titles = headers[0].split(",")
                final = []
                
                for l in listtest:
                    x = l[0].split(", ")
                
                    d = {titles[0] : x[0], titles[1]  : x[1], titles[2]  : x[2], titles[3] : x[3]}
                    final.append(d)

                objs = [
                        TeamScore(
                        user = request.user,
                        file = getFile,
                        team_name_1 = row["team_1 name"],
                        team_score_1 = row["team_1 score"],
                        team_name_2 = row["team_2 name"],
                        team_score_2 = row["team_2 score"],
                            
                        )
                        for row in final
                    ]
            
                msg = TeamScore.objects.bulk_create(objs)
                cache.clear()
                print("posting works")
                return redirect('coreapp')
            except Exception as e:
                getFile.delete()
                print(traceback.format_exc())
                logging.debug(f"Invalid file, Time : {timezone.now()}")
                logging.debug(traceback.format_exc())
                messages.error(request, "Csv file is invalid")
                return redirect('coreapp')


