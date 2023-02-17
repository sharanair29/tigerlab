from django.shortcuts import redirect
from coreapp.models import *
import io, csv, codecs
from django.contrib import messages
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
import traceback

from django.core.cache import cache

import logging
logging.basicConfig(filename="./logging.log", level=logging.DEBUG)


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
        """
        save file uploaded to Files model which is Foreign Key mapped to the TeamScore Model
        """
        create = Files.objects.create(user=request.user, file_uploaded=file)
        create.save()
        id = create.id
        """
        retrieve file object with id to save this file in the TeamScore Model in bulk import
        """
        getFile = Files.objects.get(pk=id)
        try:
            # with headers
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
        
            bulk = TeamScore.objects.bulk_create(objs)
            cache.clear()
            logging.info("Success no key error, " + f"Time : {timezone.now()}")
            print("posting works")
            return redirect('coreapp')
        except KeyError as e:
            """
            In the even of a key error the input file has no headers so we will create one
            """
            try:
                # No headers
                print(traceback.format_exc())
                logging.info("Success key fall back, " + f"Time : {timezone.now()}")
                reader = csv.reader(open(getFile.file_uploaded.path,'r',  encoding='utf-8'))
                listtest = list(reader)
                titles = ["team_1 name", "team_1 score", "team_2 name", "team_2 score"]
                final = []
                
                for l in listtest:
                    d = {titles[0] : l[0], titles[1]  : l[1], titles[2]  : l[2], titles[3] : l[3]}
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
            
                bulk = TeamScore.objects.bulk_create(objs)
                cache.clear()
                print("posting works")
                return redirect('coreapp')
            except Exception as e:
                """
                In the event that there is still an error it is safe to say the csv file is invalid 
                and formatted incorrectly. 
                Hence, we will throw an error message and log the traceback
                """
                getFile.delete()
                print(traceback.format_exc())
                logging.debug(f"Invalid file, Time : {timezone.now()}")
                logging.debug(traceback.format_exc())
                messages.error(request, "Csv file is invalid")
                return redirect('coreapp')


