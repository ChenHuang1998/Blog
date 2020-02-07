import datetime
from django.shortcuts import render_to_response, render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from myblog.forms import LoginForm,RegForm
from django.core.cache import cache
from read_statistics.utils import *
from blog.models import Blog


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
                        .values('id', 'title')\
                        .annotate(read_num_sum=Sum('read_details__read_num'))\
                        .order_by('-read_num_sum')
    return blogs[:7]


def index(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    # 获取7天热门数据的缓存
    seven_hot_data = cache.get('seven_hot_data')
    if seven_hot_data is None:
        seven_hot_data = get_7_days_hot_blogs()
        cache.set('seven_hot_data',seven_hot_data, 3600)
    return render_to_response('index.html', locals())


def login(request):
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER', reverse('index'))
    # if user is not None:
    #     auth.login(request, user)
    #     return redirect(referer)
    # else:
    #     return render(request, 'error.html',{'message': '用户名密码不正确'})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))

    else:
        login_form = LoginForm()

    return render(request, 'login.html',locals())


def register(request):
    if request.method == 'POST':
        register_form = RegForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            user = auth.authenticate(username=username,password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))

    else:
        register_form = RegForm()

    return render(request, 'register.html',locals())
