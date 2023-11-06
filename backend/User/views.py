import json
from django.http import JsonResponse
from User.models import User
import base64


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
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    req_user_name = request_dict["user_name"]
    try:
        user = User.objects.get(user_name=req_user_name)
        profile_photo = user.profile_photo
        register_date = user.register_date
        if profile_photo is None:
            return JsonResponse({"profile_photo": "None",
                                 "register_date": register_date.strftime("%Y-%m-%d")})
        else:
            return JsonResponse({"profile_photo": bytes.decode(profile_photo),
                                 "register_date": register_date.strftime("%Y-%m-%d")})
    except User.DoesNotExist:
        return JsonResponse({"match": "false"})


def register(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    req_user_name = request_dict["user_name"]
    req_password = request_dict["password"]
    try:
        User.objects.get(user_name=req_user_name)
        return JsonResponse({"is_successful": "false", "duplicate": "true"})
    except User.DoesNotExist:
        user = User(user_name=req_user_name, password=req_password)
        user.save()
        return JsonResponse({"is_successful": "true", "duplicate": "false"})


def upload_avatar(request):
    user_name = request.GET.get('user_name')
    img = request.FILES.get('file').read()
    code = base64.b64encode(img)
    try:
        user = User.objects.get(user_name=user_name)
        user.profile_photo = code
        user.save()
        return JsonResponse({"is_successful": "true"})
    except User.DoesNotExist:
        # 处理找不到用户的情况
        return JsonResponse({"is_successful": "false"})
