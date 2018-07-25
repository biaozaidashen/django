import random

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, CartModel, OrderModel, \
    OrderGoodsModel
from django.core.urlresolvers import reverse

from user.models import UserTicketModel


def home(request):
    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        mainnavs = MainNav.objects.all()
        mainmustbuys = MainMustBuy.objects.all()
        mainshops = MainShop.objects.all()
        mainshows = MainShow.objects.all()
        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mainmustbuys': mainmustbuys,
            'mainshops': mainshops,
            'mainshows': mainshows,

        }
        return render(request, 'home/home.html', data)


def mine(request):
    #个人中心
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user)
        payed, wait_pay = 0, 0
        for order in orders:
            if order.o_status == 0:
                wait_pay += 1
            if order.o_status == 1:
                payed += 1
        data = {
            'wait_pay': wait_pay,  # 待付款的订单数量
            'payed': payed,  #待收货的订单量
        }
        return render(request, 'mine/mine.html', data)


def market(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('app:market_params', args=('104749', '0', '0')))


def user_market(request, typeid, cid, sid):
    """

    :param request:
    :param typeid: 分类id
    :param cid: 子分类id
    :param sid: 排序id
    :return:
    """
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()

        if user_ticket:
        #由于market页面没有通过中间件做登录验证，所以只能通过这种方式拿到用户
            user = user_ticket.user

        else:
            user = ''
        if user:
            user_cart = CartModel.objects.filter(user=user)#返回购物车信息
        else:
            user_cart = ''
        foodtypes = FoodType.objects.all()
        #获取某分类下的商品
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid, childcid=cid)
        #重新组装全部分类的参数
        #组装结果为[['全部分类'，'0'], ['酒类':'13550'], ['饮用水':'15431']]
        foodtypes_current = foodtypes.filter(typeid=typeid).first()
        if foodtypes_current:
            childtypes = foodtypes_current.childtypenames
            childtypenames = childtypes.split('#')
            child_list = []
            for childtypename in childtypenames:
                child_type_info = childtypename.split(':')
                child_list.append(child_type_info)

        #排序
        if sid == '0': #默认排序，不做处理
            pass
        if sid == '1':
            goods = goods.order_by('productnum')# 以销量排序
        if sid == '2':
            goods = goods.order_by('-price')
        if sid == '3':
            goods = goods.order_by('price')



        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'child_list': child_list,
            'cid': cid,
            'user_cart': user_cart,
        }
        return render(request, 'market/market.html', data)


def add_cart(request):
    """添加商品到购物车"""
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')

        #判断用户是否是系统自带的anonymouseuser还是自己登录的用户（通过id来判断）
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        if user.id:
            #一个商品就是一个购物车项
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            if user_carts: #如果购物车中已经存在该商品
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num

            else:
                CartModel.objects.create(user=user, goods_id=goods_id)
                data['c_num'] = 1

            return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '当前用户没有登录，请去登录'
        return JsonResponse(data)


def sub_cart(request):
    """减少购物车用户下单商品数量"""
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        goods_id = request.POST.get('goods_id') #goods_id从js中得来
        if user.id:
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
        #如果购物车中已经存在商品信息
            if user_carts:
                if user_carts.c_num == 1:
                    #直接删除购物车的商品信息
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
                return JsonResponse(data)
            data['c_num'] = 0
            return JsonResponse(data)

        data['code'] = 403
        data['msg'] = '当前用户没有登录，请去登录'
        return JsonResponse(data)


def cart(request):
    #购物车
    if request.method == 'GET':
        #获取用户
        user = request.user
        #得到所有的购物车项
        user_carts = CartModel.objects.filter(user=user)
        data = {
            'user_carts': user_carts
        }
        return render(request, 'cart/cart.html', data)


def change_select_status(request):
    #改变商品选择状态
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id') #cart_id是购物车项id ,从js中提交上来的
        cart = CartModel.objects.filter(id=cart_id).first() #由id得到购物车项
        if cart.is_select:
            cart.is_select = False
        else:
            cart.is_select = True
        cart.save()
        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_select
        }
        return JsonResponse(data)


def all_select(request):
    #点击全选
    if request.method == 'POST':
        user = request.user
        is_select = request.POST.get('all_select')  # 初始值为1

        user_carts = CartModel.objects.filter(user=user)

        is_select = '0' if is_select == '1' else '1' #点击全选按钮后取反

        if is_select == '1':
            flag = True
            for ca in user_carts:
                ca.is_select = True  # 作用是将is_select属性值存入数据库
                ca.save()
        else:
            flag = False
            for ca in user_carts:
                ca.is_select = False
                ca.save()
        data = {
            'code': 200,
            'ids': [u.id for u in user_carts],
            'flag': flag
        }
        return JsonResponse(data)

        # if is_select == '1':
        #     user_carts.update(is_select=True)#该步骤是将点击全选按钮后的购物车项的is_select属性值修改后存入数据库
        #
        #
        #
        # else:
        #     flag = True
        #     user_carts.update(is_select=False)
        #
        # data = {
        #     'code': 200,
        #     'ids': [u.id for u in user_carts],#得到购物车项的id列表
        #     'flag': flag
        # }
        # return JsonResponse(data)


def count_price(request):
    #求总价
    if request.method == 'GET':
        user = request.user
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        count_price = 0

        for carts in user_carts:
            count_price += carts.goods.price * carts.c_num
        data = {
            'code': 200,
            'count_price': round(count_price, 3),#保留三位小数
            'msg': '请求成功',
        }
        return JsonResponse(data)



def generate_order(request):
    #下单
    if request.method == 'GET':
        user = request.user


        #选择勾选的商品进行下单
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        #判断如果购物车里没有商品则不能下单，并且返回到本页面
        if user_carts:
            s = 'sdgdyettfyhsygdvysfv134311345568'
            o_num = ''  # 订单号
            for _ in range(30):
                o_num += random.choice(s)
                # 创建订单
            order = OrderModel.objects.create(user=user, o_num=o_num)
            for carts in user_carts:
                #创建商品和订单之间的关系
                OrderGoodsModel.objects.create(goods=carts.goods, order=order, goods_num=carts.c_num)
            user_carts.delete()
            return render(request, 'order/order_info.html', {'order': order})
        else:
            return render(request, 'cart/cart.html')


def change_order_status(request):
    """修改订单状态"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        OrderModel.objects.filter(id=order_id).update(o_status=1)

        return JsonResponse({'code': 200, 'msg': '请求成功'})

def order_wait_pay(request):
    #待付款 o_status=0
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=0)
        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})




def wait_pay_to_payed(request):
    #待付款订单跳转到付款页面
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()
        return render(request, 'order/order_info.html', {'order': order})


#已付款，待收货，o_status=1
def order_payed(request):

    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=1)
        return render(request, 'order/order_list_payed.html', {'orders': orders})

