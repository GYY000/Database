"""
URL configuration for WGZForce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path
from User import views
from django.conf import settings
from django.conf.urls.static import static

# from backend.User import views

urlpatterns = [
    re_path("admin/", admin.site.urls),
    re_path("loginInterface/login", views.login),
    re_path("loginInterface/fetch_info", views.fetch_info),
    re_path("loginInterface/register", views.register),
    re_path("upload_avatar", views.upload_avatar),
    re_path("upload_ques_set", views.upload_ques_set),
    re_path("check_inside_group", views.check_inside_group),
    re_path("fetch_visible_ques_set", views.fetch_visible_ques_set),
    re_path("fetch_create_ques_set", views.fetch_create_ques_set),
    re_path("search_visible_ques_set", views.search_visible_ques_set),
    re_path("fetch_all_ques_set_in_team", views.fetch_all_ques_set_in_team),
    re_path("fetch_all_ques", views.fetch_all_ques),
    re_path("send_message", views.send_message),
    re_path("delete_message", views.delete_message),
    re_path("have_read_message", views.have_read_message),
    re_path("fetch_all_receive_message", views.fetch_all_receive_message),
    re_path(r'^post_detail/(?P<pid>\d+)$', views.post_hub_param),
    re_path("post_hub", views.post_hub),
    re_path("create_post", views.create_post),
    re_path("upload_team", views.upload_team),
    re_path("fetch_all_teams", views.fetch_all_teams),
    re_path("search_team", views.search_for_team),
    re_path("get_profile_photo", views.get_profile_photo),
    re_path("post_hub", views.post_hub),
    re_path("create_post", views.create_post),
    re_path("fetch_all_teams", views.fetch_all_teams),
    re_path("search_team", views.search_for_team),
    re_path("fetch_team_avatar", views.fetch_team_avatar),
    re_path("fetch_set_avatar", views.fetch_set_avatar),
    re_path("del_team", views.del_team),
    re_path("apply_for_team", views.apply_for_team),
    re_path("del_members", views.del_members),
    re_path("del_ques_set", views.del_ques_set),
    re_path("answer_to_req", views.answer_to_req),
    re_path("fetch_all_application", views.fetch_all_application),
    re_path("fetch_all_users_in_team", views.fetch_all_users_in_team),
    re_path("get_user_post",views.get_user_post),
    re_path("search_post",views.search_post),
    re_path("get_all_relative_person",views.get_all_relative_person),
    re_path("get_history_message",views.get_history_message),
    re_path("mark_as_read",views.mark_as_read),
    re_path("upload_ques",views.upload_ques),
    re_path("search_user",views.search_user),
    re_path("editor_upload_pic", views.upload_pic),
    re_path("update_ques",views.update_ques),
    re_path("judge_ans",views.judge_ans),
    re_path("get_recent_records",views.get_recent_records),
    re_path("get_recent_question_set",views.get_recent_question_set),
    re_path("create_set_history",views.create_set_history),
    re_path("fetch_team_info", views.fetch_team_info),
    re_path("fetch_history_team",views.fetch_history_team),
    re_path("fetch_history_applications",views.fetch_history_applications),
    re_path("send_team_message",views.send_team_message),
    re_path("add_collection",views.add_collection),
    re_path("remove_collection",views.remove_collection),
    re_path("get_collections",views.get_collections),
    re_path("in_collection",views.in_collection),
    re_path("update_team_info", views.update_team),
    re_path("delete_comment",views.delete_comment),
    re_path("delete_post",views.delete_post),
    re_path("fetch_all_future_intime_tests",views.fetch_all_future_intime_tests),
    re_path("create_exam",views.create_exam),
    re_path("participate_exam",views.participate_exam),
    re_path("fetch_exam_info",views.fetch_exam_info),
    re_path("inside_exam",views.inside_exam),
    re_path("set_admin",views.set_admin),
    re_path("is_team_admin",views.is_team_admin),
    re_path("change_password",views.change_password),
    re_path("get_do_set_history",views.get_do_set_history),
    re_path("get_do_ques_history",views.get_do_ques_history)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
