# dashboard/forms.py
from django import forms
from .models import UploadFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['uploaded_file']
