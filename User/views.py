import json
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def login(request):
    print("aaa", request)
    print(json.loads(request.body)["name"])
    return JsonResponse({"message": "111"})


def register(req):
    pass