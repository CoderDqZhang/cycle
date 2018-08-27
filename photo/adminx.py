import xadmin
import xadmin.views as xviews
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _
from photo.photo_models.account import Account,PhotoList,Competition
from django.forms import widgets

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
    list_display = ('title','sub_title'
                    ,'desc','price','vip_price',)
    exclude = ('collect_users','buy_users','like_users','collect_number','like_number','buy_number',
               'is_collect', 'is_like','is_buy','createTime','location',)
    relfield_style = 'fk_ajax'


class CompetitionAdmin(object):
    list_display = ('name','desc','start_time','end_time','is_share')
    exclude = ('read_num', 'like_num',)
    relfield_style = 'fk_ajax'

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

# class MyAdminView(object):
#     def get(self, request, *args, **kwargs):
#         pass
#
# xadmin.site.register_modelview(r'^cycle/photolist/add/',testView,name='for_test')
# xadmin.site.register_view(r'cycle/photolist/add/', testView, name='for_test')
xadmin.site.register(Competition, CompetitionAdmin)
xadmin.site.register(PhotoList, PhotoListAdmin)
xadmin.site.register(Account, AccountAdmin)

xadmin.site.register(xviews.BaseAdminView, BaseSetting)
xadmin.site.register(xviews.CommAdminView, GlobalSettings)



