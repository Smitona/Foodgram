from django.contrib import admin

from users.models import CustomUser, UserFollower


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(CustomUser)
class CustomUserAdmin(BaseAdmin):
    pass


@admin.register(UserFollower)
class UserFollowerAdmin(BaseAdmin):
    pass
