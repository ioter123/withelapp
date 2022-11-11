from django.urls import path
from .views import *

app_name = 'notice'

urlpatterns = [
    path('feed/', notice_feed),
    path('write/', notice_write),
]