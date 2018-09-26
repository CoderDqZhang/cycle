from django.conf.urls import url
import os
from cycle import settings
from photo.photo_views import acount_v, photo_v

urlpatterns = [

    url('test',photo_v.test),

    #User
    url('^wechat/login/',acount_v.verify_user),
    url('^update/userinfo/',acount_v.update_user_info),
    url('^getuserinfo/',acount_v.get_user_info),
    # url('^create/photo/',photo_v.create_photo),

    #Photo
    url('home/list/',photo_v.competitions_list),
    url('photo/list/',photo_v.photo_list),
    url('competitions/photo/',photo_v.competitions_photo_list),
    url('photo/collect/',photo_v.collect_photos),
    url('photo/buy/', photo_v.buy_photos),
    url('photo/like/',photo_v.like_photos),
    url('photo/filter/',photo_v.filter_photo),
    url('photo/search/',photo_v.search_photo)
]