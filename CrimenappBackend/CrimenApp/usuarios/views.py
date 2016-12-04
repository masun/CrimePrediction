from django.shortcuts import render
from django.http import  HttpResponse
from tweets.models import Tweets
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.http import JsonResponse

from usuarios.models import MyUser as User

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'GET':
        #Index all users
        return HttpResponse(serializers.serialize("json", User.objects.all()))
    elif request.method == 'POST':
        #Register User
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        try :
            user = User.objects.create_user(email, password) 
            user.save()
            data = serializers.serialize("json",[user])
            return HttpResponse(json.dumps(json.loads(data)[0]))
        except:
            return JsonResponse({"Error": "User couldn't be created"})

def get_user(request, id):
    if request.method == 'GET':
        #Retrieve specific user by id

        pass
    elif request.method == 'DELETE': 
        #Delete specific user by id
        pass
@csrf_exempt
def login(request):
    if request.method == 'POST':
        #login user
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({"message":"User logged in succesfully"})
        else : 
            return JsonResponse({"Error":"User couldn't be authenticated"})
@csrf_exempt
def logout(request): 
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({"message":"User logged out succesfully"})

