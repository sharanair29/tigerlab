
from django.forms import ModelForm 
from .models import *

class FileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Files
        fields = '__all__'
        exclude = ['user', 'created_at']
