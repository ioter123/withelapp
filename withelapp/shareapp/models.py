from django.db import models

# Create your models here.

class Share_Feed(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=5000)
    writer = models.CharField(max_length=255, null=False)  # 아이디
    published_date = models.DateTimeField(auto_now_add=True) # 등록(수정) 일
    view = models.IntegerField(default=0)
    like_view = models.IntegerField(default=0)