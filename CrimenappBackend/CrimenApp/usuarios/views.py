from django.shortcuts import render
from django.http import  HttpResponse
from tweets.models import Tweets
from django.core import serializers

from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return HttpResponse(serializers.serialize("json", User.objects.all()))

