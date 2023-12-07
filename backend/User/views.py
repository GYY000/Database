import json
from datetime import timezone

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from User.models import *  # fixme: 王士举修改路径
import base64
from Levenshtein import distance
import io
from PIL import Image
from django.db.models import Q
from django.conf import settings
import os
from django.utils import timezone
from datetime import timedelta



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
    introduction = request.POST.get('introduction')
    set_name = request.POST.get('set_name')
    is_public = group_name == "none"
    try:
        QuestionSet.objects.get(set_name=set_name)
        return JsonResponse({"is_successful": "false"})
    except QuestionSet.DoesNotExist:
        ques_set = QuestionSet(set_name=set_name, creator=User.objects.get(uid=user_id), is_public=is_public,
                               profile_photo=code, introduction=introduction)
        ques_set.save()
        if not is_public:
            ques_perm = QuestionSetPerm(qsid=ques_set, tid=Team.objects.get(team_name=group_name))
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
    teamIds = [_.tid for _ in teamIds]
    ques_sets = list(QuestionSet.objects.filter(is_public=True))
    for quesPerm in QuestionSetPerm.objects.all():
        if teamIds.__contains__(quesPerm.tid):
            # quesSet = QuestionSet.objects.get(qsid=quesPerm.qsid)
            if not ques_sets.__contains__(quesPerm.qsid):
                ques_sets.append(quesPerm.qsid)
    dict = {}
    id_list = []
    name_list = []
    date_list = []
    introduction_list = []
    creator_list = [qs.creator.user_name for qs in ques_sets]
    for qs in ques_sets:
        id_list.append(qs.qsid)
        name_list.append(qs.set_name)
        date_list.append(qs.create_time.strftime("%Y-%m-%d"))
        introduction_list.append(qs.introduction)
    dict["name_list"] = name_list
    dict["creator_list"] = creator_list
    dict["date_list"] = date_list
    dict["introduction_list"] = introduction_list
    dict["id_list"] = id_list
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
    create_qs_list = [QuestionSet.objects.get(qsid=creator.qsid) for creator in create_qsid_list]
    name_list = [_.set_name for _ in create_qs_list]
    date_list = [_.create_time.strftime("%Y-%m-%d") for _ in create_qs_list]
    creator_list = [_.creator.user_name for _ in create_qs_list]
    introduction_list = [_.introduction for _ in create_qs_list]
    return JsonResponse({"name_list": name_list,
                         "creator_list": creator_list,
                         "date_list": date_list,
                         "introduction_list": introduction_list})


# 相似度超过30即认为匹配
def fuzzy_match(str1, str2):
    len1, len2 = len(str1), len(str2)
    max_len = max(len1, len2)

    if max_len == 0:
        return True  # 两个空字符串被认为是相似的

    similarity = 1 - distance(str1, str2) / max_len

    return similarity > 0.3


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
    for quesPerm in QuestionSetPerm.objects.all():
        if teamIds.__contains__(quesPerm.tid):
            quesSet = QuestionSet.objects.get(qsid=quesPerm.qsid)
            if not ques_sets.__contains__(quesSet):
                ques_sets.append(quesSet)
    dict = {}
    name_list = []
    date_list = []
    creator_list = [qs.creator.user_name for qs in ques_sets]
    introduction_list = []
    for qs in ques_sets:
        name_list.append(qs.set_name)
        date_list.append(qs.create_time.strftime("%Y-%m-%d"))
        introduction_list.append(qs.introduction)
    i = 0
    while i < len(name_list):
        if not fuzzy_match(name_list[i], search_content):
            name_list.pop(i)
            creator_list.pop(i)
            date_list.pop(i)
            introduction_list.pop(i)
            i -= 1
        i += 1
    dict["name_list"] = name_list
    dict["creator_list"] = creator_list
    dict["date_list"] = date_list
    dict["introduction_list"] = introduction_list
    return JsonResponse(dict)


def fetch_all_ques(request):
    '''
前->后	    后->前
ques_set_name           除了creator、ques_set_name别的都数组返回吧
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    qs_id = request_dict['qs_id']
    qs = QuestionSet.objects.get(qsid=qs_id)
    questions = Question.objects.filter(qsid=qs_id)
    creator = QuestionSet.objects.get(qsid=qs_id).creator.user_name
    profile_photo = qs.profile_photo
    introduction = qs.introduction
    qs_name = qs.set_name
    contents = []
    scores = []
    serial_nums = []
    ques_ids = []
    for _ in questions:
        ques_ids.append(_.qid)
        contents.append(_.content)
        scores.append(_.score)
        serial_nums.append(_.serial_num)
    questions = merge_and_sort(serial_nums, scores, contents, ques_ids)
    return JsonResponse(
        {"creator": creator, "profile_photo": bytes.decode(profile_photo),
         "introduction": introduction,
         "ques_set_name": qs_name, "questions": questions})


def merge_and_sort(serial_nums, scores, contents, ques_ids):
    if len(serial_nums) != len(scores) or len(scores) != len(contents) or len(ques_ids) != len(contents):
        print("无法合并数组，长度不同!")
        return []
        # 创建空的三元组数组
    quarter_lets = []

    # 将三个数组合并为三元组数组
    for serial_num, score, content, ques_id in zip(serial_nums, scores, contents, ques_ids):
        quarter_let = {"serial_num": serial_num, "score": score, "content": content, "id": ques_id}
        quarter_lets.append(quarter_let)

    # 按照三元组中的第一个元素进行排序
    sorted_quarter_lets = sorted(quarter_lets, key=lambda x: x["serial_num"])

    return sorted_quarter_lets


from User import sensi_filter


def send_message(request):
    '''
    前->后	    后->前
sender_id	    is_successful
receiver_name
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    sender_id = request_dict["sender_id"]
    receiver_name = request_dict["receiver_name"]
    content = sensi_filter.filter(request_dict["content"])
    try:
        sender = User.objects.get(uid=sender_id)
        receiver = User.objects.get(user_name=receiver_name)
    except:
        return JsonResponse({"is_successful": "false"})
    message = Message(sender=sender, receiver=receiver, content=content)
    message.save()
    inserted_message = Message.objects.get(id=message.id)
    # 将消息对象转换为字典形式
    message_dict = {
        "is_sender": "true",
        "content": inserted_message.content,
        "time": inserted_message.time.strftime("%Y-%m-%d %H:%M"),
        "read": inserted_message.read,
        "id": inserted_message.id
    }
    return JsonResponse(message_dict)


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
    messages = Message.objects.filter(receiver=user_id)
    content_list = [_.content for _ in messages]
    sender_name_list = [_.sender.user_name for _ in messages]
    have_read_list = [_.read for _ in messages]
    time_list = [_.time.strftime("%Y-%m-%d") for _ in messages]
    return JsonResponse({"content_list": content_list, "sender_name_list": sender_name_list,
                         "time_list": time_list, "have_read_list": have_read_list})


def post_hub(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    page_no = request_dict["page_no"] - 1
    page_size = request_dict["page_size"]
    posts = Post.objects.order_by('-update_time')
    start = page_no * page_size
    end = (page_no + 1) * page_size
    if page_no * page_size >= len(posts):
        return JsonResponse([], safe=False)
    if end >= len(posts):
        end = len(posts)
    name_photos = [(_.creator.user_name, _.creator.profile_photo) for _ in
                   posts]
    arr = [{"pid": posts[i].pid, "title": posts[i].title, "creator_name": name_photos[i][0],
            "update_time": posts[i].update_time.strftime("%Y-%m-%d %H:%M"), "content": posts[i].content,
            "uid": posts[i].creator.uid} for i in range(len(posts))]
    return JsonResponse({"posts": arr[start:end], "total": len(posts)}, safe=False)


def post_hub_param(request, pid):
    if request.method == "GET":
        post = Post.objects.get(pid=pid)
        dict1 = {"pid": post.pid, "title": post.title, "creator_name": post.creator.user_name,
                 "update_time": post.update_time.strftime("%Y-%m-%d %H:%M"), "content": post.content
                 }
        comments = Comment.objects.filter(pid=pid).order_by("create_time")
        # fixme comment的时间我先按创建时间来了
        comments = [{"cid": _.id, "user_name": _.creator.user_name,
                     "uid": _.creator.uid,
                     "content": _.content,
                     "create_time": _.create_time.strftime("%Y-%m-%d %H:%M")
                     } for _ in comments]
        return JsonResponse({"post": dict1, "comment": comments})

    elif request.method == "POST":
        request_dict = json.loads(request.body.decode('utf-8'))
        print(request_dict)
        uid = request_dict["uid"]
        content = sensi_filter.filter(request_dict["content"])
        comment = Comment(creator=User.objects.get(uid=uid), content=content, pid=Post.objects.get(pid=pid))
        comment.save()
        return JsonResponse({"cid": comment.id, "user_name": comment.creator.user_name,
                             "uid": comment.creator.uid,
                             "content": comment.content,
                             "create_time": comment.create_time.strftime("%Y-%m-%d %H:%M")
                             })


def create_post(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    post = Post(creator=User.objects.get(uid=request_dict["uid"]),
                content=sensi_filter.filter(request_dict['content']),
                title=request_dict['title'])
    post.save()
    return JsonResponse({"description": "成功"})


def upload_team(request):
    '''
    前->后	后->前
user_id	                is_successful(true false)
group_name
file
introduction
url:/upload_team
    '''
    assert request.method == "POST"
    user_id = request.POST.get('user_id')
    group_name = request.POST.get('group_name')
    introduction = request.POST.get('introduction')
    if request.FILES.get('file') == None:
        code = None
    else:
        img = request.FILES.get('file').read()
        code = base64.b64encode(img)
    try:
        team = Team(team_name=group_name, creator=User.objects.get(uid=user_id), profile_photo=code,
                    introduction=introduction)
        team.save()
        #通过GROUP_name+"_VIRTUAL"来获取虚拟
        User(user_name=group_name+"_VIRTUAL",password="123456",profile_photo=code).save()
        return JsonResponse({"is_successful": "true"})
    except Exception as e:
        print(e)
        return JsonResponse({"is_successful": "false"})


def fetch_all_teams(request):
    group_name_list = []
    introduction_list = []
    creator_list = []
    date_list = []
    tid_list = []
    for _ in Team.objects.all():
        tid_list.append(_.tid)
        group_name_list.append(_.team_name)
        introduction_list.append(_.introduction)
        creator_list.append(_.creator.user_name)
        date_list.append(_.create_date.strftime("%Y-%m-%d"))
    return JsonResponse({"group_name_list": group_name_list,
                         "introduction_list": introduction_list,
                         "tid_list": tid_list,
                         "creator_list": creator_list,
                         "date_list": date_list})


def search_for_team(request):
    search_cont = json.loads(request.body.decode("utf-8"))["search_content"]
    group_name_list = []
    introduction_list = []
    creator_list = []
    date_list = []
    for _ in Team.objects.all():
        if fuzzy_match(_.team_name, search_cont):
            group_name_list.append(_.team_name)
            introduction_list.append(_.introduction)
            creator_list.append(_.creator.user_name)
            date_list.append(_.create_date.strftime("%Y-%m-%d"))
    return JsonResponse({"group_name_list": group_name_list,
                         "introduction_list": introduction_list,
                         "creator_list": creator_list,
                         "date_list": date_list})


def get_profile_photo(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    print(request_dict)
    user_name = request_dict["user_name"]
    user = User.objects.get(user_name=user_name)

    base64_photo = user.profile_photo

    if base64_photo is None:
        return JsonResponse({"profile_photo": None})

    decoded_photo = base64.b64decode(base64_photo)
    img = Image.open(io.BytesIO(decoded_photo))

    compressed_img = img.resize((300, 300))
    compressed_img_io = io.BytesIO()
    compressed_img.save(compressed_img_io, format='JPEG', quality=70)
    return JsonResponse({"profile_photo": base64.b64encode(compressed_img_io.getvalue()).decode('utf-8')})


def fetch_team_avatar(request):
    team_name = json.loads(request.body.decode("utf-8"))["team_name"]
    try:
        team = Team.objects.get(team_name=team_name)
        return JsonResponse({"avatar": bytes.decode(team.profile_photo)})
    except Exception:
        return JsonResponse({"avatar": 'none'})


def fetch_set_avatar(request):
    set_name = json.loads(request.body.decode("utf-8"))["set_name"]
    try:
        set = QuestionSet.objects.get(set_name=set_name)
        return JsonResponse({"avatar": bytes.decode(set.profile_photo)})
    except Exception:
        return JsonResponse({"avatar": 'none'})


def del_team(request):
    '''
    前->后	后->前
team_name	    is_successful(true,false)
url:/del_team
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    team_name = request_dict['team_name']
    try:
        team = Team.objects.get(team_name=team_name)
        team.delete()
        return JsonResponse({"is_successful": "true"})
    except:
        return JsonResponse({"is_successful": "false"})


def apply_for_team(request):
    '''
    前->后	后->前
creator_name（用户组创建者的名字）	is_successful(true,false)
team_name
applier_id
url:/apply_for_team
    '''
    # TODO creator_name无用？
    request_dict = json.loads(request.body.decode('utf-8'))
    creator_name = request_dict["creator_name"]
    team_name = request_dict["team_name"]
    applier_id = request_dict["applier_id"]
    joinReq = JoinRequest(uid=User.objects.get(uid=applier_id),
                          tid=Team.objects.get(team_name=team_name),
                          status="未审理,请耐心等待！")
    joinReq.save()
    return JsonResponse({"is_successful": "true"})


def del_members(request):
    '''
    前->后	后->前
del_user_id	is_successful(true,false)
team_name
url:/del_members
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    del_user_ids = request_dict["del_user_ids"]
    tid = request_dict["tid"]
    try:
        for id in del_user_ids :
            ReUserTeam.objects.get(uid=id, tid=tid).delete()
        return JsonResponse({"is_successful": "true"})
    except:
        return JsonResponse({"is_successful": "false"})


def del_ques_set(request):
    '''
前->后	后->前
ques_set_name	is_successful(true,false)
url:/del_ques_set
    '''
    request_dict = json.loads(request.body.decode('utf-8'))
    ques_set_name = request_dict["ques_set_name"]
    try:
        QuestionSet.objects.get(set_name=ques_set_name).delete()
        return JsonResponse({"is_successful": "true"})
    except:
        return JsonResponse({"is_successful": "false"})


def answer_to_req(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    id = request_dict['id']
    team_name = request_dict['team_name']
    applier_name = request_dict['applier_name']
    agree = request_dict["agree"]
    applier = User.objects.get(user_name=applier_name)
    team = Team.objects.get(team_name=team_name)
    if agree:
        try:
            ReUserTeam(uid=applier, tid=team, is_admin=False).save()
        except:
            return JsonResponse({"is_successful": "false"})
    JoinRequest.objects.get(id=id).delete()
    return JsonResponse({"is_successful": "true"})


def fetch_all_application(request):
    '''
    前->后	后->前
user_id	    applier_name_list
	        team_name_list
	        time_list
	        id_list(申请的编号们 方便删除)
url:/fetch_all_application
    '''
    request_dict = json.loads(request.body.decode("utf-8"))
    user_id = request_dict["user_id"]
    applier_name_list = []
    team_name_list = []
    time_list = []
    id_list = []
    for _ in JoinRequest.objects.all():
        if _.tid.creator.uid == user_id:
            id_list.append(_.id)
            applier_name_list.append(_.uid.user_name)
            team_name_list.append(_.tid.team_name)
            time_list.append(_.create_time.strftime("%Y-%m-%d"))
    return JsonResponse({"applier_name_list": applier_name_list,
                         "team_name_list": team_name_list,
                         "time_list": time_list,
                         "id_list": id_list})


def fetch_all_ques_set_in_team(request):
    '''
    前->后	后->前
team_name	    name_list
	        creator_list
	        introduction_list
	        date_list
url:/fetch_all_ques_set_in_team

    '''

    request_dict = json.loads(request.body.decode('utf-8'))
    tid = request_dict["tid"]
    name_list = []
    creator_list = []
    introduction_list = []
    ques_sum_list=[] #内含题目数量
    do_time_list=[]
    qsid_list = []
    date_list=[]
    avg_scores=[]
    for _ in QuestionSetPerm.objects.filter(tid=tid):
        qsid_list.append(_.qsid.qsid)
        name_list.append(_.qsid.set_name)
        creator_list.append(_.qsid.creator.user_name)
        date_list.append(_.qsid.create_time.strftime("%Y-%m-%d %H:%M"))
        introduction_list.append(_.qsid.introduction)
        ques_sum_list.append(len(list(Question.objects.filter(qsid=_.qsid.qsid))))
        shs=list(SetHistory.objects.filter(qsid=_.qsid.qsid))
        do_time_list.append(len(shs))
        sum_score=0
        for sh in shs:
            sum_score+=sh.score
        sum_score=0 if len(shs)==0 else sum_score/len(shs)
        avg_scores.append(sum_score)
    return JsonResponse({"name_list": name_list, "creator_list": creator_list,
                         "introduction_list": introduction_list,
                         "qsid_list": qsid_list,
                         "date_list": date_list,
                         "ques_sum_list": ques_sum_list,
                         "do_time_list": do_time_list,
                         "average_score_list":avg_scores
                         })


def fetch_all_users_in_team(request):
    '''
    前->后	后->前
team_name	name_list
	        register_date_list
url:/fetch_all_users_in_team
    '''
    #fixme 加个过题总数和正确率
    tid = json.loads(request.body.decode('utf-8'))['tid']
    name_list = []
    register_date_list = []
    uid_list = []
    do_prob_sum_list=[]
    accuracy_list=[]
    for _ in ReUserTeam.objects.filter(tid=tid):
        name_list.append(_.uid.user_name)
        register_date_list.append(_.join_date.strftime("%Y-%m-%d %H:%M"))
        uid_list.append(_.uid.uid)
        try:
            qhs=QuestionHistory.objects.filter(uid=_.uid.uid)
        except:
            qhs=[]
        do_prob_sum_list.append(len(list(qhs)))
        sum_scores=0
        get_scores=0
        for _ in qhs:
            sum_scores+=Question.objects.get(qid=_.qid.qid).score
            get_scores+=_.score
        accuracy_list.append(get_scores/sum_scores if len(qhs)!=0 and sum_scores!=0 else 0)
    print(uid_list)
    return JsonResponse({"name_list": name_list,
                         "register_date_list": register_date_list,
                         "uid_list": uid_list,
                         "do_prob_sum_list":do_prob_sum_list,
                         "accuracy_list":accuracy_list
                         })


def fetch_team_info(request):
    tid = json.loads(request.body.decode('utf-8'))['tid']
    team = Team.objects.get(tid=tid)
    return JsonResponse({"creator_name": team.creator.user_name,
                         "team_name": team.team_name,
                         "introduction": team.introduction,
                         "date": team.create_date,
                         "avatar":bytes.decode(team.profile_photo)})


def get_user_post(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    uid = request_dict['uid']
    page_no = request_dict['page_no'] - 1
    page_size = request_dict['page_size']
    posts = Post.objects.filter(creator=uid).order_by('-update_time')
    start = page_no * page_size
    end = (page_no + 1) * page_size
    if page_no * page_size >= len(posts):
        return JsonResponse({"total": 0, "posts": []})
    if end >= len(posts):
        end = len(posts)
    names = [_.creator.user_name for _ in posts[start:end]]
    arr = [{"pid": posts[i].pid, "title": posts[i].title, "creator_name": names[i - start],
            "update_time": posts[i].update_time.strftime("%Y-%m-%d"), "content": posts[i].content} for i in
           range(start, end)]
    return JsonResponse({"total": len(posts), "posts": arr})


def search_post(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    key_word = request_dict['key_word']
    page_no = request_dict['page_no'] - 1
    page_size = request_dict['page_size']
    posts = list(Post.objects.order_by('-update_time'))
    i = 0
    while i < len(posts):
        if (not fuzzy_match(posts[i].content, key_word)) and (not fuzzy_match(posts[i].title, key_word)):
            posts.pop(i)
            i -= 1
        i += 1
    start = page_no * page_size
    end = (page_no + 1) * page_size
    if page_no * page_size >= len(posts):
        return JsonResponse({"total": 0, "posts": []})
    if end >= len(posts):
        end = len(posts)
    names = [_.creator.user_name for _ in posts[start:end]]
    arr = [{"pid": posts[i].pid, "title": posts[i].title, "creator_name": names[i - start],
            "update_time": posts[i].update_time.strftime("%Y-%m-%d"), "content": posts[i].content, } for i in
           range(start, end)]
    return JsonResponse({"total": len(posts), "posts": arr})


def upload_ques(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    try:
        Question(creator=User.objects.get(uid=request_dict['creator_id']),
                 qsid=request_dict['qs_id'],
                 content=request_dict['content'],
                 serial_num=request_dict['serial_num'],
                 score=request_dict['score']
                 ).save()
        return JsonResponse({"is_successful": "true"})
    except:
        return JsonResponse({"is_successful": "false"})


def get_all_relative_person(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    uid = request_dict['uid']
    messages = list(Message.objects.order_by('-time'))
    i = 0
    user_names = []
    user_ids = []
    reads = []
    while i < len(messages):
        if messages[i].sender.uid == uid or messages[i].receiver.uid == uid:
            if messages[i].sender.uid != uid:
                if not user_ids.__contains__(messages[i].sender.uid):
                    user_ids.append(messages[i].sender.uid)
                    user_names.append(messages[i].sender.user_name)
                    reads.append(not messages[i].read)
            if messages[i].receiver.uid != uid:
                if not user_ids.__contains__(messages[i].receiver.uid):
                    user_ids.append(messages[i].receiver.uid)
                    user_names.append(messages[i].receiver.user_name)
                    reads.append(not messages[i].read)
        i += 1
    return JsonResponse([{"user_name": user_names[i],
                          "user_id": user_ids[i],
                          "has_unread_message": reads[i]
                          } for i in range(len(user_names))], safe=False)


def get_history_message(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    uid1 = request_dict['sender']
    uid2 = request_dict['receiver']
    messages = Message.objects.filter(Q(sender=uid1, receiver=uid2) | Q(sender=uid2, receiver=uid1)).order_by(
        '-time').reverse()
    mes_list = [{"is_sender": _.sender.uid != uid2,
                 "content": _.content, "time": _.time.strftime("%Y-%m-%d %H:%M"), "read": _.read, "id": _.id
                 } for _ in messages]
    return JsonResponse({"message_list": mes_list, "receiver": uid2}, safe=False)


def mark_as_read(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    sender_id = request_dict['sender_id']
    receiver_id = request_dict['receiver_id']
    for _ in Message.objects.all():
        print("HAHAHAHHA")
        print(_.read)
        if _.sender.uid == sender_id and _.receiver.uid == receiver_id and _.read == False:
            _.read = True
            _.save()
    return JsonResponse({"description": "成功"})


def search_user(request):
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))
    user_name1 = request_dict["user_name"]
    try:
        user = User.objects.get(user_name=user_name1)
        return JsonResponse({"has_user": True, "uid": user.uid})
    except:
        return JsonResponse({"has_user": False})


def upload_pic(request):
    image = request.FILES.get('image')
    file_name = "images/"
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, file_name))
    img_name = fs.save(image.name, image)
    # TODO:on server change here
    img_url = 'http://127.0.0.1:8000' + settings.MEDIA_URL + file_name + img_name
    return JsonResponse({'img_url': img_url})


def update_ques(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    is_delete = request_dict['is_delete']
    qid = request_dict['qid']
    if is_delete:
        Question.objects.get(qid=qid).delete()
        return JsonResponse({"is_successful": "true"})
    else:
        content = request_dict['content']
        serial_num = request_dict['serial_num']
        score = request_dict['score']
        ques = Question.objects.get(qid=qid)
        ques.content = content
        ques.serial_num = serial_num
        ques.score = score
        ques.save()
        return JsonResponse({"is_successful": "true"})

def update_team(request):
    assert request.method == "POST"
    tid = request.POST.get('tid')
    introduction = request.POST.get('introduction')
    try:
        team = Team.objects.get(tid=tid)
        team.introduction = introduction
        if request.POST.get('change_avatar') != "false":
            file = request.FILES.get('file').read()
            code = base64.b64encode(file)
            team.profile_photo = code
        team.save()
        return JsonResponse({"is_successful": "true"})
    except QuestionSet.DoesNotExist:
        return JsonResponse({"is_successful": "false"})

import math


def judge_select(ans, std, score):
    assert type(ans) == str
    assert type(std) == str
    if len(std) == 1:
        return score if ans == std else 0
    else:  # 多选
        selects = ans.split(',')
        standards = std.split(',')
        for _ in selects:
            if not standards.__contains__(_):
                return 0
        # 如果多选或者错选直接0昏
        return score * len(selects) / len(standards)  # 分数是浮点


def compute_text_score(ans, std, score):
    assert type(ans) == str
    assert type(std) == str
    len1, len2 = len(std), len(ans)
    max_len = max(len1, len2)
    if max_len == 0:
        return True  # 两个空字符串被认为是相似的
    similarity = 1 - distance(std, ans) / max_len
    return min(math.sqrt(similarity) / 0.8, 1) * score


def judge_fill(ans, std, score):
    assert type(ans) == list
    assert type(std) == list
    sum = 0
    for i in range(len(ans)):
        sum += compute_text_score(ans[i], std[i], score)
    sum /= len(ans)
    return sum


def judge_fussion(type_list, ans_list, std_list, score_list):
    scores = []
    for i in range(len(type_list)):
        if type_list[i] == '选择':
            scores.append(judge_select(ans_list[i], std_list[i], score_list[i]))
        elif type_list[i] == '填空':
            scores.append(judge_fill(ans_list[i], std_list[i], score_list[i]))
        else:
            scores.append(score_list[i])
    return scores


def judge_ans(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    qids = request_dict['qids']
    types = request_dict['types']
    answers = request_dict['answers']
    standard_ans = request_dict['standard_ans']
    all_scores = request_dict['all_scores']
    hit_scores = []
    for i in range(len(types)):
        if types[i] == '选择':
            hit_scores.append(judge_select(answers[i], standard_ans[i], all_scores[i]))
        elif types[i] == '填空':
            hit_scores.append(judge_fill(answers[i], standard_ans[i], all_scores[i]))
        elif types[i] == '问答':
            hit_scores.append(all_scores[i])
        else:
            hit_scores.append(judge_fussion(types[i], answers[i], standard_ans[i], all_scores[i]))
    return JsonResponse({"hit_scores": hit_scores})


def get_recent_records(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    uid = request_dict['uid']
    total = request_dict['total']
    qs = list(SetHistory.objects.filter(uid=uid).order_by('-time'))[:total]
    total_scores = []
    for _ in qs:
        total = 0
        questions = Question.objects.filter(qsid=_.qsid)
        for q in questions:
            total += q.score
        total_scores.append(total)

    return JsonResponse([{"question_set_name": qs[i].qsid.set_name,
                          "user_score": qs[i].score,
                          "total_score": total_scores[i],
                          "time": qs[i].time.strftime("%Y-%m-%d %H:%M")
                          } for i in range(len(qs))], safe=False)


def get_recent_question_set(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    total = request_dict['total']
    user_id = request_dict["uid"]
    teamIds = list(ReUserTeam.objects.filter(uid=user_id))
    teamIds = [_.tid for _ in teamIds]
    ques_sets = list(QuestionSet.objects.filter(is_public=True))
    set_team_map = {}
    for quesPerm in QuestionSetPerm.objects.all():
        if teamIds.__contains__(quesPerm.tid):
            # quesSet = QuestionSet.objects.get(qsid=quesPerm.qsid)
            if not ques_sets.__contains__(quesPerm.qsid):
                set_team_map[quesPerm.qsid.qsid] = quesPerm.tid.team_name
                ques_sets.append(quesPerm.qsid)
    ques_sets = sorted(ques_sets, key=lambda x: x.create_time, reverse=True)[:total]
    dic = [{"question_set_name": _.set_name,
            "time": _.create_time.strftime("%Y-%m-%d %H:%M"),
            "is_public": _.is_public,
            "team_name": None if _.is_public else set_team_map[_.qsid]
            } for _ in ques_sets]
    return JsonResponse(dic, safe=False)


def create_set_history(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    scores = request_dict['scores']
    qids = request_dict['qids']
    qsid = request_dict['qsid']
    uid = request_dict['uid']
    answers = request_dict['answers']
    scores_sum = sum(scores)
    set_history = SetHistory(uid=User.objects.get(uid=uid),
                             qsid=QuestionSet.objects.get(qsid=qsid),
                             score=scores_sum)
    set_history.save()
    for i in range(len(qids)):
        QuestionHistory(shid=set_history, score=scores[i], answer=str(answers[i]),
                        qid=Question.objects.get(qid=qids[i]),uid=User.objects.get(uid=uid)).save()
    return JsonResponse({"is_successful": "true"})


#这里我需要返回最近的最多五条，组内成员做组内题集的记录
def fetch_history_team(request):
    request_dict=json.loads(request.body.decode('utf-8'))
    tid=request_dict['tid']
    shs=list(SetHistory.objects.order_by('-time'))
    question_sets=QuestionSetPerm.objects.filter(tid=tid)
    question_sets=[_.qsid for _ in question_sets]
    ans=[]
    for _ in shs:
        if question_sets.__contains__(_.qsid):
            ans.append(_)
    ans=ans[:5]
    name_list=[_.uid.user_name  for _ in ans]
    ques_set_list=[_.qsid.set_name for _ in ans]
    date_list=[_.time.strftime("%Y-%m-%d %H:%M") for _ in ans]
    return JsonResponse({"user_name_list":name_list,"ques_set_list":ques_set_list,
                         "date_list":date_list})


#返回最近七天的申请进入该组申请数
def fetch_history_applications(request):
    request_dict=json.loads(request.body.decode('utf-8'))
    tid=request_dict['tid']
    now=timezone.now()
    seven_days_ago=now-timedelta(days=7)
    reqs=list(JoinRequest.objects.filter(tid=tid).filter(create_time__gte=seven_days_ago))
    return JsonResponse({"application_sum":len(reqs)})


def send_team_message(request):
    request_dict=json.loads(request.body.decode('utf-8'))
    tid=request_dict['tid']
    uid_list=request_dict['uid_list']
    message=request_dict['message']
    team=Team.objects.get(tid=tid)
    try:
        sender=User.objects.get(user_name=team.team_name+"_VIRTUAL")
    except:
        tmp=User(user_name=team.team_name+"_VIRTUAL",password="123456",profile_photo=team.profile_photo)
        tmp.save()
        sender=tmp
    for uid in uid_list:
        Message(sender=sender,receiver=User.objects.get(uid=uid),content=message).save()
    return JsonResponse({"is_successful":"true"})