from django.shortcuts import render
from django.http import  HttpResponse
from tweets.models import Tweets

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get(request, id):
    t = Tweets.objects.filter(id = id).values()
    return HttpResponse(t)