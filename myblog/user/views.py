from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from user.forms import LoginForm, RegForm


# Create your views here.

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

    return render(request, 'user/login.html', locals())


def login_for_modal(request):
    data = {}
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'success'
    else:
        data['status'] = 'error'
    return JsonResponse(data)


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

    return render(request, 'user/register.html', locals())


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from'), reverse('index'))


def user_info(request):
    return render(request, 'user/user_info.html', locals())
