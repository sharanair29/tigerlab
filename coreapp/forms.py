
from django.forms import ModelForm 
from .models import *

class TeamScoreForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeamScoreForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = TeamScore
        fields = '__all__'
        required_fields = ['team_name_1', 'team_score_1', 'team_name_2', 'team_score_2']
        exclude = ['user', 'file']
