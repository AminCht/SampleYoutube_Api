from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'MEMBERSHIP_STATUS']
    list_editable = ['MEMBERSHIP_STATUS']

    def first_name(self, appUser:models.AppUser):
        return appUser.user.first_name

    def last_name(self, appUser:models.AppUser):
        return appUser.user.last_name


