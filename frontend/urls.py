# coding=utf8

from django.urls import path

from frontend.views import (special_views)

urlpatterns = [
    path('', special_views.page_not_found),
    path('health_check', special_views.health_check),
]

# 登陆注册
urlpatterns += [

]
