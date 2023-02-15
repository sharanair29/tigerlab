from django.contrib import admin
from .models import *
# Register your models here.

class FilesAdmin(admin.ModelAdmin):
    list_display=('user', 'file_uploaded', 'created_at')
admin.site.register(Files, FilesAdmin)

class TeamScoreAdmin(admin.ModelAdmin):
    list_display=('team_name_1','team_score_1', 'team_name_2', 'team_score_2')
admin.site.register(TeamScore, TeamScoreAdmin)