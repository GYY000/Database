import json
from django.http import JsonResponse


# Create your views here.
def login(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    user_name = request_dict["username"]
    password = request_dict["password"]
    print(user_name)
    if user_name == "gyy" and password == "123456":
        return JsonResponse({"match": "true"})
    else:
        return JsonResponse({"match": "false"})


def fetch_info(request):
    return JsonResponse({"profile_photo": "1", "register_date": "2023.10.31"})


def register(request):
    return JsonResponse({"is_successful": "true", "duplicate": "false"})
