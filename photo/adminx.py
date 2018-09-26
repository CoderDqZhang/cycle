import xadmin
import xadmin.views as xviews
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _
from photo.photo_models.account import Account,PhotoList,Competition,Photo
from django.forms import widgets
from photo.utils import upload_qiniu
from cycle import settings
from xadmin.views.base import ModelAdminView, filter_hook, csrf_protect_m


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    enable_themes = True
    site_title = "赛事管理后台"
    site_footer = "赛事管理后台"
    # menu_style = 'accordion'

    # 菜单设置

    def get_site_menu(self):
        return (

            {'title': '数据类型', 'perm': self.get_model_perm(Account, 'change'), 'menus': (
                {'title': '用户管理', 'icon': 'fa fa-user'
                    , 'url': self.get_model_url(Account, 'changelist')},
                {'title': '照片管理', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(PhotoList, 'changelist')},
                {'title': '赛事管理', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(Competition, 'changelist')},
            )},

        )

class AccountAdmin(object):
    list_display = ('user','nickname','openid','avatar','createTime'
                    ,'gender','phone','vip',)

    relfield_style = 'fk_ajax'

class PhotoListAdmin(object):
    list_display = ('title','price','vip_price',)
    exclude = ('collect_users','buy_users','like_users','collect_number','like_number','buy_number',
               'is_collect', 'is_like','is_buy','createTime','location','photos','sub_title'
                    ,'desc','user')
    relfield_style = 'fk_ajax'
    change_form_template = 'xadmin/photo/PhotoList/change_form.html'

    add_form_template = 'xadmin/photo/PhotoList/add_form.html'

    def save_models(self):
        obj = self.new_obj
        print(obj)
        obj.save()
        # flag = self.obj is None and 'create' or 'change'
        # self.log(flag, self.change_message(), self.obj)

        for afile in self.request.FILES.getlist('photos_multiple'):
            url,url_s = upload_qiniu.qiniu_upload_comparess("Competition", afile)
            photo_info = upload_qiniu.get_image_info(settings.MEDIA_URL1 + url)
            photo_info_s = upload_qiniu.get_image_info(settings.MEDIA_URL1 + url_s)
            print(photo_info_s['height'])
            photo = Photo.objects.create(url=settings.MEDIA_URL1 + url,s_url= settings.MEDIA_URL1 + url_s,
                                         width=photo_info['width'], height=photo_info['height'],
                                         s_height=photo_info_s['height'], s_width=photo_info_s['width']
                                         )
            obj.photos.add(photo)


class CompetitionAdmin(object):
    list_display = ('name','desc','start_time','end_time','is_share',)
    exclude = ('read_num', 'like_num','photos')
    relfield_style = 'fk_ajax'  # fk-外键 显示样式
    change_form_template = 'xadmin/photo/competition/change_form.html'
    add_form_template = 'xadmin/photo/competition/add_form.html'
    # def get_context(self):
    #     return

    def save_models(self):
        obj = self.new_obj
        print(obj)
        obj.save()
        # flag = self.obj is None and 'create' or 'change'
        # self.log(flag, self.change_message(), self.obj)

        for afile in self.request.FILES.getlist('photos_multiple'):
            url,url_s = upload_qiniu.qiniu_upload_comparess("Competition", afile)
            photo_info = upload_qiniu.get_image_info(settings.MEDIA_URL1 + url)
            photo_info_s = upload_qiniu.get_image_info(settings.MEDIA_URL1 + url_s)
            photo_info_s['height']
            print('ddddd')
            print(photo_info_s)
            photo = Photo.objects.create(url=settings.MEDIA_URL1 + url,s_url= settings.MEDIA_URL1 + url_s,
                                         width = photo_info['width'], height = photo_info['height'],
                                         s_height = photo_info_s['height'], s_width = photo_info_s['width'])
            obj.photos.add(photo)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(Competition, CompetitionAdmin)
xadmin.site.register(PhotoList, PhotoListAdmin)
xadmin.site.register(Account, AccountAdmin)

xadmin.site.register(xviews.BaseAdminView, BaseSetting)
xadmin.site.register(xviews.CommAdminView, GlobalSettings)



