from django.shortcuts import render
from django.http import  HttpResponse
from tweets.models import Tweets
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from usuarios.models import MyUser as User

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'GET':
      print request.content_params
    elif request.method == 'POST':
      print request.body
    return HttpResponse(serializers.serialize("json", User.objects.all()))

