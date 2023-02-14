from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime 
from django.utils import timezone
# Create your models here.

class Files(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_uploaded = models.FileField(upload_to='files')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username