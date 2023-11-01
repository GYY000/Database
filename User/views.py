import json
from django.shortcuts import render
from django.http import JsonResponse
from User.models import *

# Create your views here.
def login(request):
    print("aaa", request)
    print(json.loads(request.body)["name"])
    user = User(user_name="zj", password="123456")
    user.save()
    return JsonResponse({"message": "111"})


def register(req):
    pass