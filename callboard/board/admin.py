from django.contrib import admin
from django.contrib.auth.models import User
from .models import Announcement, Category, Comment, Profile
# Register your models here.

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.register(User, UserAdmin)
admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Comment)


