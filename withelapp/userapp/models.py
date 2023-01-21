# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .choice import *


class UserManager(BaseUserManager):

    def create_user(self, user_id, password, name, nickname, phone, email, birth, address, gender, introduce, level, auth,
                    **extra_fields):
        if not user_id:
            raise ValueError('email Required!')

        user = self.model(
            user_id=user_id,
            name=name,
            nickname=nickname,
            phone=phone,
            email=email,
            birth=birth,
            address=address,
            gender=gender,
            introduce=introduce,
            level=level,
            auth=auth,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, name=None, nickname=None, phone=None, email=None, birth=None, address=None, gender=None, introduce=None, level=None, auth=None):
        user = self.create_user(user_id, password, name, nickname, phone, email, birth, address, gender, introduce, level, auth)
        
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    user_id = models.CharField(max_length=128, verbose_name="아이디", null=True, unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    name = models.CharField(max_length=128, verbose_name='이름')
    nickname = models.CharField(max_length=128, blank=True, null=True, verbose_name='닉네임')
    phone = models.CharField(max_length=128, blank=True, null=True, verbose_name='연락처')
    email = models.EmailField(max_length=256, blank=True, null=True, verbose_name='이메일')
    birth = models.CharField(max_length=256, blank=True, null=True, verbose_name='생년월일')
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name='주소')
    gender = models.CharField(choices=GENDER_CHOICES,max_length=20, blank=True, null=True, verbose_name='성별')
    introduce = models.CharField(max_length=256, blank=True, null=True, verbose_name='소개')
    level = models.CharField(choices=LEVEL_CHOICES,max_length=20, blank=True, null=True, verbose_name='등급')
    auth = models.CharField(max_length=10, blank=True, null=True, verbose_name='인증번호')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일', null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, verbose_name='마지막 로그인 날짜', null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False, verbose_name='탈퇴여부')

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "user"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"