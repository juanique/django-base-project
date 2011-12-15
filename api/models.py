from django.db import models

# Create your models here.
class UserProfile(models.Model):
    facebook_id = models.CharField(max_length=32)
