from django.urls import path,re_path
from blog.views import *


urlpatterns = [
    path('',blog_list,name='blog_list'),
    path('<int:blog_pk>/', blog_detail,name='blog_detail'),
    path('type/<int:blogs_type_pk>',blogs_with_type,name='blogs_with_type')

]