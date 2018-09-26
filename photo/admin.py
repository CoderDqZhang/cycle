from django.contrib import admin
from photo.photo_models.account import Account,PhotoList,Competition,Photo
from photo.utils import upload_qiniu
from cycle import settings

# Register your models here.
class CompetitionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        for afile in request.FILES.getlist('photos_multiple'):
            url,url_s = upload_qiniu.qiniu_upload_comparess("Competition", afile)
            photo = Photo.objects.create(url=settings.MEDIA_URL1 + url,s_url= settings.MEDIA_URL1 + url_s)
            obj.photos.add(photo)

class AccountAdmin(admin.ModelAdmin):
    pass

class PhotoListAdmin(admin.ModelAdmin):
    pass

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Account)
admin.site.register(PhotoList)
