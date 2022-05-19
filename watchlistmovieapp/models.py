from pyexpat import model
from unicodedata import name
from django.db import models

from django.contrib.auth.models import User

# Create your models here.




class userdetail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    idFilm = models.IntegerField(null=True)
    action = models.CharField(max_length=50)
    titleFilm = models.CharField(max_length=50)
    note = models.CharField(default="",max_length=500)
    last_updated = models.DateTimeField(auto_now_add=True)

   


class watchList(models.Model):
    
    idFilm = models.IntegerField(null=True)
    addUser = models.CharField(default="",max_length=50)
    last_updated = models.DateTimeField(auto_now_add=True)

  