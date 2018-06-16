from django.contrib import admin
from .models import Offer
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

admin.site.register(Offer)

class UserProfileInline(admin.StackedInline):
 model = Profile
 max_num = 1
 can_delete = False

class UserAdmin(AuthUserAdmin):
 inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
