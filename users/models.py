# from statistics import mode
from os import truncate
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User)


    def __str__(self):
        return self.name

class Message(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.title
