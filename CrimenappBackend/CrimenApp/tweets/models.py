from __future__ import unicode_literals

from django.db import models
import json
import jsonpickle



class TweetsManager(models.Manager):
    def create_tweet(self, texto, fecha=None, que=None, como=None, donde=None, cuando=None):
        book = self.create(texto=texto, fecha=fecha, que=que, como=como, donde=donde, cuando=cuando)
        return book





# Create your models here.

class Tweets(models.Model):
    cuando = models.CharField(max_length=256, null=True)
    donde = models.CharField(max_length=256, null=True)
    como = models.CharField(max_length=256, null=True)
    que = models.CharField(max_length=256, null=True)
    texto = models.CharField(max_length=256, unique=True, null=True)
    fecha = models.DateTimeField(null=True)


    objects = TweetsManager()

    def __str__(self):
        return "Tweet : %s\n" % self.texto