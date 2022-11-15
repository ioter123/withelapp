from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'password',
        'name',
        'nickname',
        'phone',
        'email',
        'birth',
        'address',
        'gender',
        'introduce',
        'level',
        'auth',
        'is_active',
        'created_at',
        'updated_at',
        'last_login',
        'is_admin',
        'is_out',
    )
    list_display_links = (
        'user_id',
        'password',
        'name',
        'nickname',
        'phone',
        'email',
        'birth',
        'address',
        'gender',
        'introduce',
        'level',
        'auth',
        'is_active',
        'created_at',
        'updated_at',
        'last_login',
        'is_admin',
        'is_out',
    )

    search_fields = [
        'user_id',
        'password',
        'name',
        'nickname',
        'phone',
        'email',
        'birth',
        'address',
        'gender',
        'introduce',
        'level',
        'auth',
        'is_active',
        'created_at',
        'updated_at',
        'last_login',
        'is_admin',
        'is_out',
    ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
