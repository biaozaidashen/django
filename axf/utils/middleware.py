from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import UserModel, UserTicketModel

'''
中间件验证用户是否已经成功登录，因为用户登录成功后会生成ticket,所以可通过它来验证
只能通过验证后才能进入个人中心
'''


class Middle(MiddlewareMixin):

    def process_request(self, request):
        #验证cookie中的ticket，验证不通过，跳转到登录页面
        #验证通过，request.user代表当前登录的用户信息
        #return None 或者不写return

        path = request.path #请求的url
        need_login = ['/app/mine/', '/app/addCart/',
                      '/app/subCart/', '/app/cart/',
                      '/app/generateOrder/', '/app/waitPay/',
                      '/app/payed/', '/app/count_price/',
                      '/app/allSelect/']#个人中心页面是需要登录验证的

        if path in need_login:
            #先获取cookies中的ticket
            ticket = request.COOKIES.get('ticket')
            if not ticket:
                return HttpResponseRedirect(reverse('user:login'))
            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
            if user_ticket:
                #获取到有认证的相关信息
                #1.验证当前认证信息是否过期，如果没过期，request.user赋值
                #2.如果过期了，跳转到登录，并删除认证信息
                if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                    #datetime.utcnow()与user_ticket.out_time类型不同不能进行比较，必须user_ticket.out_time把tzinfo设为None它们才是相同的类型
                    #过期
                    UserTicketModel.objects.filter(user=user_ticket.user).delete()
                    return HttpResponseRedirect(reverse('user:login'))
                else:
                    #没有过期，把当前用户赋给request.user, 并且删除多余的认证信息
                    request.user = user_ticket.user
                    #删除多余的认证信息，也就是说把之前登录时保留下来的老的ticket删除，最后服务器只保留最新的ticket

                    UserTicketModel.objects.filter(Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()
                    return None
            else:
                return HttpResponseRedirect(reverse('user:login'))
        else:
            return None

