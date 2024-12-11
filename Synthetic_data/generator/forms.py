from django import forms
from .models import Metadata, Synthesizer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class MetadataForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ['name', 'description', 'file']


class SynthesizerForm(forms.ModelForm):
    class Meta:
        model = Synthesizer
        fields = ['name', 'metadata']

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
