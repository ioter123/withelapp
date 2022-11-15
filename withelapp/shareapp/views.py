from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# 같은 폴더
from .models import *

# 유틸
from datetime import datetime, timedelta
# Create your views here.

def share_feed(request):
    vAllFeed = Share_Feed.objects.all()

    if vAllFeed.count() != 0:
        vAllFeed = vAllFeed.filter().order_by('published_date')

    context = {
        'feed' : vAllFeed
    }
    return render(request, 'share/share_feed.html', context)