import json
from django.shortcuts import render
from django.http import JsonResponse

import User

# Create your views here.
def login(request):
    print("aaa", request)
    print(json.loads(request.body)["name"])
    User
    return JsonResponse({"message": "111"})


def register(req):
    pass