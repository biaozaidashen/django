from django.conf.urls import url

from app import views

urlpatterns = [
    #首页
    url(r'^home/', views.home, name='home'),
    #个人中心
    url(r'^mine/', views.mine, name='mine'),
    #闪购超市
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.user_market, name='market_params'),

    #添加购物车商品数量
    url(r'^addCart/', views.add_cart, name='addCart'),
    #减少购物车商品数量
    url(r'^subCart/', views.sub_cart, name='subCart'),
    #购物车页面
    url(r'^cart/', views.cart, name='cart'),
    #修改购物车中商品的选择情况
    url(r'^changeSelectStatus/', views.change_select_status, name='change'),
    #下单
    url(r'^generateOrder/', views.generate_order, name='generate_order'),
    #改变订单状态
    url(r'^changeOrderStatus/', views.change_order_status, name='change_order_status'),
    #待付款订单
    url(r'^waitPay/', views.order_wait_pay, name='order_wait_pay'),
    #待收货
    url(r'^payed/', views.order_payed, name='order_payed'),
    #待付款订单支付
    url(r'^waitPayToPayed/', views.wait_pay_to_payed, name='wait_pay_to_payed'),
    #全选购物车的商品
    url(r'^allSelect/', views.all_select, name='all_select'),
    #总价
    url(r'^count_price/', views.count_price, name='count_price'),
]