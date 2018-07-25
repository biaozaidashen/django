from datetime import datetime, timedelta
import random
from django.contrib.auth.hashers import make_password, check_password

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from user.models import UserModel, UserTicketModel

'''
在注册的时候加密必须在后台加密， 而验证密码与确认密码是否一致可以在js中验证
'''


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        password = request.POST.get('password')
        icon = request.FILES.get('icon') #获取头像文件用FILES

        if not all([username, email, password, icon]):
            msg1 = '注册信息必须填写完整'
            return render(request, 'user/user_register.html', {'msg1': msg1})

        password = make_password(password)  # 加密操作
        UserModel.objects.create(username=username, password=password, email=email, icon=icon)

        return HttpResponseRedirect(reverse('user:login'))#重定向时冒号后面不能有空格


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = UserModel.objects.filter(username=username).first()
        if user:
            if check_password(password, user.password):#验证输入的密码是否正确

                #1.保存ticket在客户端
                ticket = ''
                s = 'qwertyuiopasdfghjklasdasaasdaw'
                for _ in range(28):
                    ticket += random.choice(s)
                response = HttpResponseRedirect(reverse('app:mine'))
                out_time = datetime.now() + timedelta(days=14) #过期期限是14天
                response.set_cookie('ticket', ticket, expires=out_time)#expires表示cookie的有效期限

                #2.保存ticket在服务器后台
                UserTicketModel.objects.create(user=user, out_time=out_time, ticket=ticket)


                return response

            else:
                msg2 = '密码错误'
                return render(request, 'user/user_login.html', {'msg2': msg2})
        else:
            msg3 = '用户不存在'
            return render(request, 'user/user_login.html', {'msg3': msg3})


def logout(request):
    if request.method == 'GET':
        # request.user.ticket = None  #删除服务器里的ticket值
        # request.user.save()
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket') #注销后浏览器cookie里的ticket也会删除
        return response







