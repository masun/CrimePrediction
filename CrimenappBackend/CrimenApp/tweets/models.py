from __future__ import unicode_literals

from django.db import models
import json
import jsonpickle

# Create your models here.

class Tweets(models.Model):
    cuando = models.CharField(max_length=128)
    donde = models.CharField(max_length=128)
    como = models.CharField(max_length=128)
    que = models.CharField(max_length=128)
    texto = models.CharField(max_length=140)
    fecha = models.DateTimeField()

    # @classmethod
    # def create(self, cuando, donde, como, que, texto, fecha):
    #     tweet = self(cuando=cuando, donde=donde, como=como, que=que, texto=texto, fecha=fecha)
    #     return tweet

    @classmethod 
    def toJSON(self):
        return jsonpickle.encode(self)      

    # @classmethod
    # def __unicode__(self):
    #     # s = "cuando:" + self.cuando + "\n"
    #     # s += "donde:" + self.donde + "\n"
    #     # s += "como:" + self.como + "\n"
    #     # s += "que:" + self.que + "\n"
    #     # s += "texto:" + self.texto + "\n"
    #     # s += "fecha:" + self.fecha + "\n" 
    #     return u'%s' % self.texto