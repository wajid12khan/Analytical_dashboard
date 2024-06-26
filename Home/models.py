from django.db import models

# Create your models here.
# dashboard/models.py
from django.db import models

class UploadFile(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
