import json
from django.http import JsonResponse
from User.models import User, QuestionSet, QuestionSetPerm, Team
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
                                 "register_date": register_date.strftime("%Y-%m-%d"),
                                 "user_id": user.uid})
        else:
            return JsonResponse({"profile_photo": bytes.decode(profile_photo),
                                 "register_date": register_date.strftime("%Y-%m-%d"),
                                 "user_id": user.uid})
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
    user_id = request.GET.get('user_id')
    img = request.FILES.get('file').read()
    code = base64.b64encode(img)
    try:
        user = User.objects.get(uid=user_id)
        user.profile_photo = code
        user.save()
        return JsonResponse({"is_successful": "true"})
    except User.DoesNotExist:
        # 处理找不到用户的情况
        return JsonResponse({"is_successful": "false"})


def upload_ques_set(request):
    assert request.method == "POST"
    file = request.FILES.get('file')
    code = base64.b64encode(file)
    user_id = request.POST.get('user_id')
    group_name = request.POST.get('group_name')
    set_name = request.POST.get('set_name')
    is_public = "group_name" == "none"
    ques_set = QuestionSet(set_name=set_name, creator=user_id, is_public=is_public,
                           profile_photo=code)
    ques_set.save()
    if not is_public:
        ques_id = QuestionSet.objects.get(set_name=set_name).qsid
        ques_perm = QuestionSetPerm(qsid=ques_id,tid=Team.objects.get(team_name=group_name).tid)
        ques_perm.save()
    return JsonResponse({"is_successful": "true"})
