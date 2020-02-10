from django.urls import path
from likes.views import *
urlpatterns = [
    path('like_change', like_change, name='like_change')
]