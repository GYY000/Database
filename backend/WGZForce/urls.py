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
#from backend.User import views

urlpatterns = [
    re_path("admin/", admin.site.urls),
    re_path("loginInterface/login", views.login),
    re_path("loginInterface/fetch_info", views.fetch_info),
    re_path("loginInterface/register", views.register),
    re_path("upload_avatar", views.upload_avatar),
    re_path("upload_ques_set", views.upload_ques_set),
    re_path("check_inside_group",views.check_inside_group),
    re_path("fetch_visible_ques_set",views.fetch_visible_ques_set),
    re_path("fetch_create_ques_set",views.fetch_create_ques_set),
    re_path("search_visible_ques_set",views.search_visible_ques_set),
    re_path("fetch_all_ques",views.fetch_all_ques),
    re_path("send_message",views.send_message),
    re_path("delete_message",views.delete_message),
    re_path("have_read_message",views.have_read_message),
    re_path("fetch_all_receive_message",views.fetch_all_receive_message),
    re_path("post_hub",views.post_hub),
    re_path(r'^post_hub/(?P<pid>\d+)/$',views.post_hub_param),
    re_path("create_post",views.create_post),
]
