import json
from django.http import JsonResponse
from User.models import User


# Create your views here.
def login(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    req_user_name = request_dict["user_name"]
    req_password = request_dict["password"]
    try:
        user = User.objects.get(user_name=req_user_name)
        password = user.password
        if password == req_password:
            return JsonResponse({"match": "true"})
        else:
            return JsonResponse({"match": "false"})
    except User.DoesNotExist:
        return JsonResponse({"match": "false"})



def fetch_info(request):
    # TODO just for test 需要连入数据库
    return JsonResponse({"profile_photo": "1", "register_date": "2023.10.31"})


def register(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    req_user_name = request_dict["user_name"]
    req_password = request_dict["password"]
    user = User.objects.filter(user_name=req_user_name)
    if len(user) != 0:
        return JsonResponse({"is_successful": "false", "duplicate": "true"})
    else:
        user = User(user_name=req_user_name, password=req_password)
        user.save()
        return JsonResponse({"is_successful": "true", "duplicate": "false"})
