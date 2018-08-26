from django.contrib import admin
from photo.photo_models.account import Account,PhotoList,Competition

# Register your models here.
@admin.register
class CompetitionAdmin(admin.ModelAdmin):
    pass

class AccountAdmin(admin.ModelAdmin):
    pass

class PhotoListAdmin(admin.ModelAdmin):
    pass

admin.site.register(Account)
admin.site.register(PhotoList)
admin.site.register(Competition)
