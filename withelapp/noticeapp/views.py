from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# 같은 폴더
from .models import *

# 유틸
from datetime import datetime, timedelta

# 로그인 유저 정보 가져오기
from django.contrib.auth import login
# Create your views here.


def currnet_user(request):
    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    user_info = {
        'id' : user_id,
        'name' : user_name
                 }
    return user_info

def notice_feed(request):
    vAllFeed = Notice_Feed.objects.all()

    if vAllFeed.count() != 0:
        vAllFeed = vAllFeed.filter().order_by('published_date')

    context = {
        'feed' : vAllFeed
    }
    return render(request, 'notice/notice_feed.html', context)

def notice_write(request):

    if request.method == 'POST':
        content = request.POST.get('content')
        title = request.POST.get('title')
        writer = 'test'
        published_date = datetime.today()
        view = 0
        like_view = 0

        Notice_Feed.objects.create(
            title = title,
            content = content,
            writer = writer,
            published_date = published_date,
            view = view,
            like_view = like_view
        )

        return redirect('/notice/feed')
        print('저장완료')


    return render(request, 'notice/notice_write.html')