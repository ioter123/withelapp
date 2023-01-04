from django.urls import path
from .views import *

app_name = 'share'

urlpatterns = [
    path('feed/', share_feed, name='feed'),
    # path('write/', share_write, name='write'),
]