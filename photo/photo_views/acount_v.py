from photo.utils import define
import importlib
import json
import sys
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse
from photo.photo_models.account import Account

def verify_user(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.WE_CHAT_LOGIN)
        if checkrequest is None:
            code = body['code']
            openid = define.getopenid(code)
            print(openid)
            try:
                user = Account.objects.get(openid=openid)
                print(user)
                data['user'] = model_to_dict(user)
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                try:
                    user_ins =  User.objects.get(username=openid)
                except :
                    user_ins = User.objects.create_user(
                        username=openid,
                        password=openid
                    )
                    user_ins.save()
                    user_ins.is_active = True
                print(body['avatar'])

                account = Account.objects.create(
                    user=user_ins,
                    openid=openid
                )
                data['user'] = model_to_dict(Account.objects.get(openid=openid))
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)

def update_user_info(request):
    if request.method == 'POST':
        openid = json.loads(request.body.decode('utf-8'))['openid']
        try:
            user = Account.objects.get(openid=openid)
            body, checkrequest = define.request_verif(request,define.UPDATA_USER_INFO)
            if checkrequest is None:
                user.nickname = body['nickname']
                user.phone = body['phone']
                user.province = body['province']
                user.avatar = body['avatar']
                user.save()
                data = {}
                data['user'] = model_to_dict(user)
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data)


def get_user_info(request):
    if request.method == 'POST':
        openid = json.loads(request.body.decode('utf-8'))['openid']
        try:
            user = Account.objects.get(openid=openid)
            body, checkrequest = define.request_verif(request,define.GET_USER_INFO)
            if checkrequest is None:
                data = {}
                # return  AccountSerializer
                data['user'] = model_to_dict(user)
                return  JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在",None))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data)


def return_userinfo(data):
    json = model_to_dict(data,exclude=['avatar'])
    json['avatar'] = define.MEDIAURL + str(data.avatar)
    return json
