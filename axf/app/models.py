from django.db import models

from user.models import UserModel


class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  # 通用id

    class Meta:
        abstract = True


class MainWheel(Main):
    """轮播"""

    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    """导航栏"""

    class Meta:
        db_table = "axf_nav"


class MainMustBuy(Main):
    """必购"""

    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    categoryid = models.CharField(max_length=16)  # 分类名称
    brandname = models.CharField(max_length=100)  # 分类名称

    img1 = models.CharField(max_length=200)  # 图片
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)  # 商品名称
    price1 = models.FloatField(default=0)  # 原价格
    marketprice1 = models.FloatField(default=1)  # 折后价格

    img2 = models.CharField(max_length=200)  # 图片
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)  # 商品名称
    price2 = models.FloatField(default=0)  # 原价格
    marketprice2 = models.FloatField(default=1)  # 折后价格

    img3 = models.CharField(max_length=200)  # 图片
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)  # 商品名称
    price3 = models.FloatField(default=0)  # 原价格
    marketprice3 = models.FloatField(default=1)  # 折后价格

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    #商品
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 规格
    price = models.FloatField(default=0)  # 折后价格
    marketprice = models.FloatField(default=1)  # 原价
    categoryid = models.CharField(max_length=16)  # 分类id
    childcid = models.CharField(max_length=16)  # 子分类id
    childcidname = models.CharField(max_length=100)  # 名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)  # 销量排序

    class Meta:
        db_table = 'axf_goods'

#购物车相当于是用户与商品之间的中间表
#用户与购物车的关系是一对一
#商品与购物车的关系是多对一，一个购物车项对应一个商品

class CartModel(models.Model):
    """购物车"""
    #重要说明：  在该表格中，不同的id表示不同的购物车项，而不是购物车
    user = models.ForeignKey(UserModel)  # 关联用户
    goods = models.ForeignKey(Goods)  # 关联商品
    c_num = models.IntegerField(default=1)  # 商品个数
    is_select = models.BooleanField(default=True)  # 是否选择

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    """订单"""
    user = models.ForeignKey(UserModel)  # 关联用户
    o_num = models.CharField(max_length=64)  # 订单编号
    # 0代表已下单， 但是未付款 ，1已付款未发货， 2已付款，已发货
    o_status = models.IntegerField(default=0)  # 状态
    o_create = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    #订单和商品的中间表
    goods = models.ForeignKey(Goods) #关联商品
    order = models.ForeignKey(OrderModel)  # 关联订单
    goods_num = models.IntegerField(default=1)  # 商品个数

    class Meta:
        db_table = 'axf_order_goods'






