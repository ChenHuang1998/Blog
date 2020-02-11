from django.urls import path
from user.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('user_info/', user_info, name='user_info'),
    path('login_for_modal/', login_for_modal, name='login_for_modal'),
    path('register/', register, name='register'),
]