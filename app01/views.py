from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01 import models


# Create your views here.

def home(request):
    if request.method == 'GET':
        response = {}

        # top 10（公告）的处理，筛选10个也要改
        announcements = models.Announcement.objects.filter()
        # 把这10个公告封装成字典
        a_list = []
        for a in announcements:
            dic = {'a_id': a.a_id, 'a_title': a.a_title}
            a_list.append(dic)
        # 把列表装进回复字典里
        response['a_list'] = a_list

        # 帖子推荐列表，推荐8个帖子，推荐8个要改
        recommends = models.Topic.objects.filter(recommend=True)
        # 推荐列表
        r_list = []
        for t in recommends:
            dic = {'t_id': t.t_id, 't_title': t.t_title, 't_introduce': t.t_introduce, 't_photo': t.t_photo}
            r_list.append(dic)
        # 把列表装进response
        response['r_list'] = r_list

        return render(request, 'home.html', **response)


def all_tie(request):
    if request.method == 'GET':
        # 默认时间排序把帖子传过去
        topics = models.Topic.objects.filter()
        return render(request, 'all.html', {'topics': topics})

    elif request.method == 'POST':
        # 搜索接收一个字段，查询标题或者简介里有关键字的帖子
        keys = request.POST.get('keys')
        # 按关键字查询标题里含有关键字的
        topics = models.Topic.objects.filter(t_title__icontains=keys)
        return render(request, 'all.html', {'topics': topics})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        # 验证用户名密码是否正确，然后登陆存入session
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        if len(models.User.objects.filter(uid=uid, password=pwd)) != 0:
            # 登录成功
            request.session['uid'] = uid
            redirect('/home')
            pass
        else:
            # 登录失败
            return render(request, 'login.html', {'message': '用户名或者密码错误'})
            pass


def register(request):
    if request.method == 'POST':
        # 判断是否已有
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        if len(models.User.objects.filter(uid=uid)) != 0:
            # 已被创建，返回错误
            return render(request, 'login.html', {'message': '用户名已被创建'})
        else:
            # 插入数据
            user = {
                'uid': uid,
                'password': pwd,
            }
            models.User.objects.create(**user)
            return redirect('/home')


def publish(request):
    if request.method == 'GET':
        return render(request, 'publish.html')
    elif request.method == 'POST':
        # session获取uid
        # 提交发布的文章
        pass


def single(request):
    if request.method == 'GET':
        return render(request, 'publish.html')
    elif request.method == 'POST':
        # 进行回复
        pass
