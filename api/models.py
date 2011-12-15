from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    #genre = models.CharField(max_length=1)
    #birth = models.DateField()
    #breed = models.ForeignKey(Breed)
    
    def __unicode__(self):
		return self.name
    def save(self, *args, **kwargs):
        return super(Pet, self).save(*args, **kwargs)
        
class Breed(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
		return self.name
		
# Missing Pet Profile
