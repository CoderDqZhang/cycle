import xadmin
import xadmin.views as xviews
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _
from photo.photo_models.account import Account,PhotoList,Competition
from django.forms import widgets

# Register your models here.

# class UserProfileAdmin(UserAdmin):
#     def get_form_layout(self):
#         if self.org_obj:
#             self.form_layout = (
#                 Main(
#                     Fieldset('',
#                              'username', 'password',
#                              css_class='unsort no_title'
#                              ),
#                     Fieldset(_('Personal info'),
#                              Row('first_name', 'last_name'),
#                              'email'
#                              ),
#                     Fieldset(_('Permissions'),
#                              'groups', 'user_permissions'
#                              ),
#                     Fieldset(_('Important dates'),
#                              'last_login', 'date_joined'
#                              ),
#                 ),
#                 Side(
#                     Fieldset(_('Status'),
#                              'is_active', 'is_staff', 'is_superuser',
#                              ),
#                 )
#             )
#         return super(UserAdmin, self).get_form_layout()

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "赛事管理后台"
    site_footer = "赛事管理后台"

    # def get_site_menu(self):
    #     return (
    #         {'title': '数据管理', 'perm': self.get_model_perm(Account, 'change'),
    #             'menus':
    #                 ({'title': '用户', 'url': self.get_model_url(Account, 'changelist'),
    #                   'icon':'fa fa-vimeo-square'},
    #                  {'title': '照片', 'url': self.get_model_url(PhotoList, 'changelist'),
    #                   'icon': 'fa fa-vimeo-square'},
    #                  {'title': '赛事', 'url': self.get_model_url(Competition, 'changelist'),
    #                   'icon':'fa fa-vimeo-square'}
    #                  )},
    #     )
    # menu_style = "accordion"

class AccountAdmin(object):
    list_display = ('user','nickname','openid','avatar','createTime'
                    ,'gender','phone','vip',)
    list_exclude = ('read_num','like_num',)


class PhotoListAdmin(object):

    # readonly_fields = ('big_images','thumer_images',)
    list_display = ('createTime','title','sub_title'
                    ,'desc','location','location','price','vip_price','is_collect'
                    ,'is_like','collect_number','like_number',)
    list_exclude = ('collect_users','buy_users','like_users',)
    # relfield_style = ('user','collect_users','buy_users','like_users',)
    relfield_style = 'fa-ajax'

    # def preview(self, obj):
    #     # 第二处替换： 'xadmin:blog_post_change'
    #     url_edit = urlresolvers.reverse('admin:blog_post_change', args=(obj.id,))
    #     return u'''
    #                 <span><a href="/%s.html" target="_blank">预览</a></span>
    #                 <span><a href="%s" target="_blank">编辑</a></span>
    #             ''' % (obj.alias, url_edit)
    #
    # preview.short_description = u'操作'
    # preview.allow_tags = True


# def change_view(self, request, object_id, extra_context=None):
#         print(extra_context)
#         return super(self,request, object_id, extra_context)
#
#     def save_model(self, request, object_id, extra_context=None):
#         field = ('big_images','thumer_images',)
#         return super(self, request, object_id, extra_context)
#
#     def display_img(self, obj):
#         url = obj.big_images
#         return '<img ref="%s" />' % url
#
#     display_img.short_description = '用户照片'
#     display_img.allow_tags = True


class CompetitionAdmin(object):
    filter_vertical = ('user','competition',)
    list_display = ('name','desc','start_time','end_time','is_share')

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



