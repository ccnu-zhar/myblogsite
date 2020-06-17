from django.shortcuts import render ,redirect
from read_statistics.utils import get_seven_days_read_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(blog_content_type)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates

    return render(request,'home.html',context)

def login(request):
    '''
    username = request.POST.get('username','')
    password = request.POST.get('password', '')
    user = auth.authenticate(request,username = username,password = password)
    # 请求头 信息  reverse 反向解析
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request,user)

        return redirect(referer)
    else:
        return render(request,'error.html',{'message':'用户名或密码不正确'})
'''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from',reverse('home')))
            else:
                login_form.add_error(None,'用户名或密码不正确')
                context = {}
                context['login_form'] = login_form
                return render(request, 'login.html', context)

        else:
            context = {}
            context['login_form'] = login_form
            return render(request, 'login.html', context)
    else:
        login_form = LoginForm()
        context = {}
        context['login_form'] = login_form
        return render(request,'login.html',context)


def register(request):
     if request.method == 'POST':
         reg_form = RegForm(request.POST)
         if reg_form.is_valid():
             username = reg_form.cleaned_data['username']
             email = reg_form.cleaned_data['email']
             password = reg_form.cleaned_data['password']
             user = User.objects.create_user(username,email,password)
             user.save()
             # 注册后登陆
             user = auth.authenticate(username = username,password = password)
             auth.login(request,user)
             return redirect(request.GET.get('from', reverse('home')))

     else:
         reg_form = RegForm()

     context = {}
     context['reg_form'] = reg_form
     return render(request,'register.html',context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('form',reverse('home')))

def user_info(request):
    context = {}
    return render(request,'user_info.html',context)
