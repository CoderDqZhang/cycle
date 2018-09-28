# -*- coding: utf-8 -*-
import importlib
import sys
from django.contrib.auth.models import User
from django.db import models
from photo.utils import define

importlib.reload(sys)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField('用户名', max_length=200)  # 用户名
    openid = models.CharField(max_length=200, primary_key=True)
    avatar = models.ImageField('头像', upload_to="avatar/%Y/%m", default=u"image/default.png", max_length=200, null=True)
    createTime = models.DateField(auto_created=True, auto_now_add=True)
    gender = models.IntegerField('性别', choices=define.GENDER, default=0, null=True)
    phone = models.CharField('电话', max_length=11, default='', null=True)
    vip = models.BooleanField('是否会员',default=False)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = '用户列表'
        verbose_name_plural = '用户列表'
    # def upload_avatar(self):
    #     from django.utils.safestring import mark_safe
    #     # mark_safe后就不会转义
    #     return mark_safe("<a href=https://home.cnblogs.com/u/derek1184405959/>上传头像</a>")
    # upload_avatar.short_description = "上传头像"

class Photo(models.Model):
    url = models.CharField('照片地址', max_length=200, blank=True, null=True )
    s_url = models.CharField('水印照片地址', max_length=200, blank=True, null=True)
    s_width = models.IntegerField('照片宽', max_length=200, blank=True, null=True )
    s_height = models.IntegerField('照片高', max_length=200, blank=True, null=True)
    width = models.IntegerField('照片宽', max_length=200, blank=True, null=True)
    height = models.IntegerField('照片高', max_length=200, blank=True, null=True)
    is_buy = models.IntegerField('是否喜欢', default=0,null=True)

    def __str__(self):
        return self.url

class Competition(models.Model):
    photos = models.ManyToManyField(Photo, verbose_name='照片', blank=True,null=True)
    name = models.CharField('标题', max_length=200, blank=True, null=True)
    desc = models.TextField('介绍', blank=True, null=True)
    start_time = models.DateField('开始时间')
    end_time = models.DateField('结束时间')
    read_num = models.IntegerField('阅读数量',default=0)
    like_num = models.IntegerField('喜欢数量',default=0)
    is_share = models.BooleanField('是否推荐',default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '赛事列表'
        verbose_name_plural = '赛事列表'


class PhotoList(models.Model):
    photos = models.ManyToManyField(Photo, verbose_name='照片', blank=True,null=True)
    user = models.ManyToManyField(Account, verbose_name='创建用户', blank=True,null=True)
    createTime = models.DateField('创建时间', auto_created=True, auto_now_add=True)
    competition = models.ManyToManyField(Competition, verbose_name='赛事', blank=True,null=False)
    title = models.CharField('标题', max_length=200)  # 标题
    sub_title = models.CharField('副标题', max_length=200)  # 副标题
    desc = models.TextField('图片介绍', max_length=200)  # 副标题
    location = models.CharField('地点', max_length=200)  # 地点
    tags = models.CharField('标签', max_length=200)  # 大图
    price = models.FloatField("费用", default=0)  #费用
    vip_price = models.FloatField("vip费用", default=0)  #费用
    is_collect = models.IntegerField('是否收藏',default=0)
    is_like = models.IntegerField('是否喜欢', default=0)
    is_buy = models.IntegerField('是否喜欢', default=0)
    collect_number = models.IntegerField('收藏人数',default=0)
    like_number = models.IntegerField('喜欢人数', default=0)
    buy_number = models.IntegerField('喜欢人数', default=0)
    collect_users = models.ManyToManyField(Account, related_name='收藏用户', blank=True,null=True)
    buy_users = models.ManyToManyField(Account, related_name='购买用户', blank=True, null=True)
    like_users = models.ManyToManyField(Account, related_name='喜欢用户', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '照片列表'
        verbose_name_plural = '照片列表'

