from django.urls import path
from comment.views import *

urlpatterns = [
    path('update_comment', update_comment, name='update_comment')
]