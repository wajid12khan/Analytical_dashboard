# Home/admin.py
from django.contrib import admin
from .models import UploadFile  # Import the UploadFile model

admin.site.register(UploadFile)  # Register the UploadFile model
