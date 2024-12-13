from django.db import models
from django.contrib.auth.models import User

class Settings(models.Model):
    type = models.CharField(max_length=100)
    value = models.TextField()

class Metadata(models.Model):
    table_name = models.CharField(max_length=100)
    metadata_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields as needed

