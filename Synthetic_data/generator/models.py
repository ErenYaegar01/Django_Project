from django.db import models
from django.contrib.auth.models import AbstractUser

class Metadata(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='metadata/')
    created_at = models.DateTimeField(auto_now_add=True)
    
class Synthesizer(models.Model):
    name = models.CharField(max_length=255)
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
    model_file = models.FileField(upload_to='models/')
    created_at = models.DateTimeField(auto_now_add=True)

class ExcelFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)  # Add the name field
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.username})"  # Fallback to username if name is blank









