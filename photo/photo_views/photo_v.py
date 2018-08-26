from photo.utils import define
from django.shortcuts import render
import importlib
import json
import sys
from PIL import Image  #pip install pillow
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse
from photo.photo_models.account import Account,PhotoList,Competition
from photo.utils import upload_qiniu
from django.db.models import Q
from photo.photo_views import acount_v
from photo.libs import image_tools
from cycle import settings

# def create_photo(request):
#     if request.method == 'POST':
#         # print(request.POST)
#         # 初始化返回的字典
#         data = {}
#         # 获取小程序数据
#         body, checkrequest = define.request_verif(request, define.CREATE_PHOTO)
#         if checkrequest is None:
#             openid = body['openid']
#             try:
#                 user = Account.objects.get(openid=openid)
#                 files = request.FILES.get("photo", None)
#                 images, images_c = upload_qiniu.qiniu_upload_comparess("photo", files)
#                 photo = PhotoList.objects.create(
#                     title = body['title'],
#                     sub_title = body['sub_title'],
#                     location = body['location'],
#                     tags = body['tags'],
#                     thumer_images = images,
#                     big_images = images_c,
#                     desc = body['desc'],
#                     price = body['price'],
#                     vip_price = body['vip_price'],
#                 )
#                 photo.user.add(user)
#                 photo.save()
#                 data['user'] = model_to_dict(user)
#                 return JsonResponse(define.response("success", 0, None, data))
#             except Account.DoesNotExist:
#                 data['message'] = '用户不存在'
#                 return JsonResponse(define.response("success", 0, None, data))
#             else:
#                 return JsonResponse(define.response("success", 0, checkrequest))
#     else:
#         return JsonResponse(define.response("success",0,"请使用POST方式请求"))
#     return JsonResponse(data)

def photo_list(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.PHOTO_LIST)
        print(checkrequest)
        if checkrequest is None:
            openid = body['openid']
            try:
                user = Account.objects.get(openid=openid)
                competitions = Competition.objects.all()
                data['competitions'] = []
                for photo in competitions:
                    data['competitions'].append(return_comptitions(data=photo, openid=openid))
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                data['message'] = '用户不存在'
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)

def competitions_photo_list(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.COMPTITIONS_PHOTO_LIST)
        print(checkrequest)
        if checkrequest is None:
            openid = body['openid']
            try:
                user = Account.objects.get(openid=openid)
                photos = PhotoList.objects.filter(competition=body['comptitions_id'])
                data['photos'] = []
                for photo in photos:
                    data['photos'].append(return_photos(data=photo, openid=openid))
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                data['message'] = '用户不存在'
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)

def search_photo(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.SEARCH_LIST)
        print(checkrequest)
        if checkrequest is None:
            openid = body['openid']
            try:
                user = Account.objects.get(openid=openid)
                photos = PhotoList.objects.filter(Q(title__exact=body['title']) |
                                                  Q(desc__exact=body['title']) |
                                                  Q(sub_title_exact=body['title']) |
                                                  Q(location__exact=body['title']) |
                                                  Q(user__nickname__exact=body['title']))
                data['photos'] = []
                for photo in photos:
                    data['photos'].append(return_photos(data=photo, openid=openid))
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                data['message'] = '用户不存在'
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)

def filter_photo(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.FILTER_LIST)
        if checkrequest is None:
            openid = body['openid']
            try:
                user1 = Account.objects.get(openid=openid)
                sort_type = body['type']
                if sort_type == 1:
                    photos = PhotoList.objects.all().order_by('-like_number')
                else:
                    photos = PhotoList.objects.all().order_by('-collect_number')
                data['photos'] = []
                for photo in photos:
                    data['photos'].append(return_photos(data=photo, openid=openid))
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                data['message'] = '用户不存在'
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)


def collect_photos(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.PHOTO_COLLECT)
        print(checkrequest)
        if checkrequest is None:
            openid = body['openid']
            try:
                user = Account.objects.get(openid=openid)
                photo = PhotoList.objects.get(id=body['id'])
                if body['action'] == 'add':
                    photo.collect_users.add(user)
                else:
                    photo.collect_users.remove(user)
                photo['collect_number'] = photo.collect_users.all().count()
                photo.save()
                data['photo'] = return_photos(data=photo, openid=openid)
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                data['message'] = '用户不存在'
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)

def like_photos(request):
    if request.method == 'POST':
        data = {}
        body, checkrequest = define.request_verif(request, define.PHOTO_LIKE)
        print(checkrequest)
        if checkrequest is None:
            openid = body['openid']
            try:
                user = Account.objects.get(openid=openid)
                photo = PhotoList.objects.get(id=body['id'])
                if body['action'] == 'add':
                    photo.like_users.add(user)
                else:
                    photo.like_users.remove(user)
                photo['like_number'] = photo.collect_users.all().count()
                photo.save()
                data['photo'] = return_photos(data=photo, openid=openid)
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                data['message'] = '用户不存在'
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)

def return_comptitions(data,openid):
    json = model_to_dict(data)
    return json

def return_photos(data,openid):
    json = model_to_dict(data,exclude=['user','buy_users',
                                       'collect_users','like_users','big_images','competition'])
    json['user'] = []
    json['collect_users'] = []
    json['like_users'] = []
    json['like_number'] = data.like_users.all().count()
    json['collect_number'] = data.collect_users.all().count()
    json['buy_number'] = data.buy_users.all().count()
    if data.collect_users.all().filter(openid=openid).count() == 0:
        json['is_collect'] = False
    else:
        json['is_collect'] = True
    if data.like_users.all().filter(openid=openid).count() == 0:
        json['is_like'] = False
    else:
        json['is_like'] = True
    if data.buy_users.all().filter(openid=openid).count() == 0:
        print(str(data.big_images))
        if Image.open('./media/logo_watermark/' + str(data.big_images)):
            json['image'] = define.MEDIAURL + 'logo_watermark/' + str(data.big_images)
        else:
            im = Image.open(settings.MEDIA_ROOT + "/" + str(data.big_images))
            im_c = image_tools.logo_watermark(im, './media/logo/logo.png')
            im_c.save('./media/logo_watermark/' + str(data.big_images))
            print(im_c)
        json['is_buy'] = False
    else:
        json['image'] = define.MEDIAURL + str(data.big_images)
        json['is_buy'] = True
    for user in data.user.all():
        json['user'].append(acount_v.return_userinfo(user))
    for user in data.collect_users.all():
        json['collect_users'].append(acount_v.return_userinfo(user))
    for user in data.like_users.all():
        json['like_users'].append(acount_v.return_userinfo(user))

    print(json)
    return json