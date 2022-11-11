from django.db import models

# 유틸
from datetime import datetime, timedelta
class Notice_Feed(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=5000)
    writer = models.CharField(max_length=255, null=False)  # 아이디
    published_date = models.DateTimeField(null=False) # 등록(수정) 일
    view = models.IntegerField(default=0)
    like_view = models.IntegerField(default=0)
'''
# class notice_board(models.Model):
#     index = models.IntegerField(unique=True)
#     content = models.TextField(max_length=5000, null=True)
#     title = models.CharField(max_length=255)
#     category = models.CharField(),
#     writer = models.CharField(),  # 닉네임 최대길이
#     published_date = models.DateTimeField(),  # 등록(수정) 일
#     status = models.IntegerField(max_length=3),  # 삭제, 숨김, 표시 여부
#     view = models.IntegerField(null=True, default=0)
#
#
# class share_board(models.Model):
#     index = models.IntegerField(unique=True)
#     content = models.TextField(max_length=5000, null=True)
#     title = models.CharField(max_length=255)
#     category = models.CharField(),
#     writer = models.CharField(),  # 닉네임 최대길이
#     published_date = models.DateTimeField(),  # 등록(수정) 일
#     status = models.IntegerField(max_length=3),  # 삭제, 숨김, 표시 여부
#     view = models.IntegerField(null=True, default=0)


class Photo_board(models.Model):
    index = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=5000, null=True)
    link = models.TextField()
    writer = models.CharField(),  # 닉네임 최대길이
    published_date = models.DateTimeField(),  # 등록(수정) 일
    status = models.IntegerField(max_length=3),  # 삭제, 숨김, 표시 여부
    view = models.IntegerField(null=True, default=0)


class Reply(models.Model):
    index = models.IntegerField(unique=True)
    content = models.TextField(max_length=5000, null=True)
    writer = models.CharField(),  # 닉네임 최대길이
    published_date = models.DateTimeField(), # 등록(수정) 일
    status = models.IntegerField(max_length=3),  # 삭제, 숨김, 표시 여부

'''
