from django.db import models


# 비어있어도 되는 값? blank=True, null=True

# Create your models here.



# Q.여러 종류의 게시판? 1개의 테이블 이용하여 구현?
# Q.태그는 어디에?
# Q.작성날짜와 수정날짜 관리를 왜 같이 안하는지?

# 게시판 화면에 보여줄 요소
class board(models.Model):
    category = models.CharField(max_length=255),
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=5000, null=True)
    writer = models.CharField(),  # 닉네임 최대길이
    published_date = models.DateTimeField(), # 등록(수정) 일
    status = models.IntegerField(max_length=3),  # 삭제, 숨김, 표시 여부
    view = models.IntegerField(null=True, default=0)

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