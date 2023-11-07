import json
from django.http import JsonResponse
from models import *  # fixme: 王士举修改路径
import base64
from Levenshtein import distance


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
    file = request.FILES.get('file').read()
    code = base64.b64encode(file)
    user_id = request.POST.get('user_id')
    group_name = request.POST.get('group_name')
    set_name = request.POST.get('set_name')
    is_public = "group_name" == "none"
    try:
        QuestionSet.objects.get(set_name=set_name)
        return JsonResponse({"is_successful": "false"})
    except QuestionSet.DoesNotExist:
        ques_set = QuestionSet(set_name=set_name, creator=User.objects.get(uid=user_id), is_public=is_public,
                               profile_photo=code)
        ques_set.save()
        if not is_public:
            ques_id = QuestionSet.objects.get(set_name=set_name).qsid
            ques_perm = QuestionSetPerm(qsid=ques_id, tid=Team.objects.get(team_name=group_name).tid)
            ques_perm.save()
        return JsonResponse({"is_successful": "true"})


def check_inside_group(request):
    '''
前->后	    后->前
user_id	    is_inside(true false)
group_name
    '''
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict["user_id"]
    group_name = request_dict["group_name"]
    group = Team.objects.get(team_name=group_name)
    group_id = group.tid
    try:
        ReUserTeam.objects.get(tid=group_id, uid=user_id)
        return JsonResponse({"is_inside": "true"})
    except:
        return JsonResponse({"is_inside": "false"})


def fetch_visible_ques_set(request):
    '''
    获取所有该用户可见的问题组的信息（包括公开的和他所在的组里面的）(返回值里包含问题组的名称 创建者 还有头像）
    前->后	后->前
user_id	    name_list
	    avatar_list
	    creator_list
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict["user_id"]
    teamIds = list(ReUserTeam.objects.filter(uid=user_id))
    ques_sets = list(QuestionSet.objects.filter(is_public=True))
    for quesPerm in QuestionSetPerm.objects:
        if teamIds.__contains__(quesPerm.tid):
            quesSet = QuestionSet.objects.get(qsid=quesPerm.qsid)
            if not ques_sets.__contains__(quesSet):
                ques_sets.append(quesSet)
    dict = {}
    name_list = []
    avatar_list = []
    date_list = []
    creator_list = [User.objects.get(uid=qs.creator).user_name for qs in ques_sets]
    for qs in ques_sets:
        name_list.append(qs.set_name)
        avatar_list.append(qs.profile_photo)
        date_list.append(qs.create_time.strftime("%Y-%m-%d"))
    dict["name_list"] = name_list
    dict["avator_list"] = avatar_list
    dict["creator_list"] = creator_list
    dict["date_list"] = date_list
    return JsonResponse(dict)


def fetch_create_ques_set(request):
    '''
    前->后	后->前
user_id	    name_list
	        avatar_list
	        creator_list
获取所有该用户创建的问题组的信息(返回值里包含问题组的名称 创建者 还有头像）

    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict["user_id"]
    create_qsid_list = QuestionSet.objects.filter(creator=user_id)
    create_qs_list = [QuestionSet.objects.get(qsid=qsid) for qsid in create_qsid_list]
    name_list = [_.set_name for _ in create_qs_list]
    avatar_list = [_.profile_photo for _ in create_qs_list]
    creator_list = [User.objects.get(uid=_.creator).user_name for _ in create_qs_list]
    return JsonResponse({"name_list": name_list, "avatar_list": avatar_list,
                         "creator_list": creator_list})


# 相似度超过50即认为匹配
def fuzzy_match(str1, str2):
    len1, len2 = len(str1), len(str2)
    max_len = max(len1, len2)

    if max_len == 0:
        return True  # 两个空字符串被认为是相似的

    similarity = 1 - distance(str1, str2) / max_len

    return similarity > 0.5


def search_visible_ques_set(request):
    '''
    前->后	    后->前
user_id	        name_list
search_content	avatar_list
	            creator_list
    '''

    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict["user_id"]
    teamIds = list(ReUserTeam.objects.filter(uid=user_id))
    search_content = request_dict["search_content"]
    ques_sets = list(QuestionSet.objects.filter(is_public=True))
    for quesPerm in QuestionSetPerm.objects:
        if teamIds.__contains__(quesPerm.tid):
            quesSet = QuestionSet.objects.get(qsid=quesPerm.qsid)
            if not ques_sets.__contains__(quesSet):
                ques_sets.append(quesSet)
    dict = {}
    name_list = []
    avatar_list = []
    creator_list = [User.objects.get(uid=qs.creator).user_name for qs in ques_sets]
    for qs in ques_sets:
        name_list.append(qs.set_name)
        avatar_list.append(qs.profile_photo)
    i = 0
    while i < len(name_list):
        if not fuzzy_match(name_list[i], search_content):
            name_list.pop(i)
            avatar_list.pop(i)
            creator_list.pop(i)
            i -= 1
        i += 1
    dict["name_list"] = name_list
    dict["avator_list"] = avatar_list
    dict["creator_list"] = creator_list
    return JsonResponse(dict)


def fetch_all_ques(request):
    '''
前->后	    后->前
ques_set_name           除了creator、ques_set_name别的都数组返回吧
    '''
    # todo
    request_dict = json.loads(request.body.decode('utf-8'))
    qs_name = request_dict['ques_set_name']
    qs_id = QuestionSet.objects.get(set_name=qs_name).qsid
    questions = Question.objects.filter(qsid=qs_id)
    creator = User.objects.get(uid=questions[0].creator).user_name
    contents = []
    scores = []
    serial_nums = []
    for _ in questions:
        contents.append(_.content)
        scores.append(_.score)
        serial_nums.append(_.serial_num)
    return JsonResponse({"creator": creator, "ques_set_name": qs_name, "scores": scores,
                         "contents": contents, "serial_nums": serial_nums})


def send_message(request):
    '''
    前->后	    后->前
sender_id	    is_successful
receiver_name
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    sender_id = request_dict["sender_id"]
    receiver_name = request_dict["receiver_name"]
    content = request_dict["content"]
    try:
        sender = User.objects.get(uid=sender_id)
        receiver = User.objects.get(user_name=receiver_name)
    except:
        return JsonResponse({"is_successful": "false"})
    message = Message(sender=sender.uid, receiver=receiver.uid, content=content)
    message.save()
    return JsonResponse({"is_successful": "true"})


def delete_message(request):
    '''
    前->后	    后->前
message_id  	is_successful
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    message_id = request_dict["message_id"]
    try:
        message = Message.objects.get(id=message_id)
        message.delete()
        return JsonResponse({"is_successful": "true"})
    except Message.DoesNotExist:
        print(f"Message with id {message_id} does not exist.")
        return JsonResponse({"is_successful": "false"})


def have_read_message(request):
    '''

前->后	        后->前
message_id	    is_successful
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    message_id = request_dict["message_id"]
    try:
        message = Message.objects.get(id=message_id)
    except:
        return JsonResponse({"is_successful": "false"})
    return JsonResponse({"is_successful": ("true" if message.read else "false")})


def fetch_all_receive_message(request):
    '''

前->后	    后->前
user_id	    content_list
	        time_list
	        sender_name_list
	        have_read_list(是否已读)
    '''

    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict["user_id"]
    messages = Message.objects.filter(recevier=user_id)
    content_list = [_.content for _ in messages]
    sender_name_list = [User.objects.get(uid=_.sender).user_name for _ in messages]
    have_read_list = [_.read for _ in messages]
    time_list = [_.time for _ in messages]
    return JsonResponse({"content_list": content_list, "sender_name_list": sender_name_list,
                         "time_list": time_list, "have_read_list": have_read_list})


def post_hub(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    page_no = request_dict["page_no"]
    page_size = request_dict["page_size"]
    posts = list(Post.objects.order_by('-update_time'))
    start = page_no * page_size
    end = (page_no + 1) * page_size
    if page_no * page_size >= len(posts):
        return JsonResponse([], safe=False)
    if end >= len(posts):
        end = len(posts)
    name_photos = [(User.objects.get(uid=_.creator).user_name, User.objects.get(uid=_.creator).profile_photo) for _ in
                   posts]
    arr = [{"pid": posts[i].pid, "title": posts[i].title, "creator_name": name_photos[i][0],
            "update_time": posts[i].update_time, "content": posts[i].content,
            "profile_photo": name_photos[i][1]} for i in range(len(posts))]
    return JsonResponse(arr[start:end], safe=False)


def post_hub_param(request, pid):
    if request.method == "GET":
        post = Post.objects.get(pid=pid)
        dict1 = {"pid": post.pid, "title": post.title, "creator_name": User.objects.get(uid=post.creator).user_name,
                 "update_time": post.update_time, "content": post.content,
                 "profile_photo": User.objects.get(uid=post.creator).profile_photo}
        comments = Comment.objects.filter(pid=pid).order_by("create_time")
        # fixme comment的时间我先按创建时间来了
        comments = [{"cid": _.id, "user_name": User.objects.get(uid=_.creator).user_name,
                     "content": _.content, "profile_photo": User.objects.find(uid=_.creator).profile_photo,
                     "create_time": _.create_time
                     } for _ in comments]
        return JsonResponse({"post": dict1, "comment": comments})

    elif request.method == "POST":
        request_dict = json.loads(request.body.decode('utf-8'))
        uid = request_dict["uid"]
        content = request_dict["pid"]
        comment = Comment(creator=uid, content=content, pid=pid)
        comment.save()
        return JsonResponse({"description": "成功"})


def create_post(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    post = Post(creator=request_dict['uid'],
                content=request_dict['content'],
                title=request_dict['title'])
    post.save()
    return JsonResponse({"description": "成功"})
