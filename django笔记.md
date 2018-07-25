

####创建虚拟环境

1.

`pip instatll virtualenv`



`virtualenv --no-site-packages djangoenv`

`virtualenv --no-site-packages -p  python版本号  env`

`pip freeze:查看pip安装过的包`

`pip list：查看所有安装过的包`



先装一下库：
`pip install django==1.11`
`pip install pymysql`

2.

` python -m venv 虚拟文件名`

进入虚拟环境的scripts脚步激活虚拟环境

` activate`

退出激活

` deactivate`

3. 建一个文件 re_install.txt 存放安装包,然后递归安装全部需要的包

`pip isntall -r re_install.txt`

#### 创建项目并且运行



```
django-amdin startproject day1 创建项目

python manage.py startapp app   创建应用

python manage.py runserver  运行项目

```



### MVT关系模型



各个模块的交互关系
Django收到HTTP请求后，依次完成下列处理：

根据URL通过URLConf模块映射到View函数，将HttpRequest对象作为参数传入。
在View函数中，获取HTTP请求的参数，通过Model访问数据库，进行业务逻辑运算得到输出数据。
然后，加载Template，根据输出数据生成页面，将HttpResponse对象返回。

生成迁移

`python manage.py makemigrations 应用名`

执行迁移

`python manage.py migrate`

创建django自带的超级管理员账号

`python manage.py createsuperuser`

用户跟踪的三种方式:

- cookie(在请求头里)
- 隐藏域(在表单里)
- URL重写(URL里加额外信息向服务器提供身份标识，字节最多为2048)



##### settings.py 配置文件：

​	

```
installed_app

databases

static

tempalets

media

rest_framework

login_url

logger
```



##### urls.py： 总的一个路由

例子：

```
urlpatterns = [
    url('^admin/', admin.site.urls),
    url(r'^app/', include('app.urls', namespace='app')),
    url(r'^user/', include('user.url', namespace='user'))
]
```

应用app的路由：

```
urlpatterns = [
url(r'^grade/', views.grade, name='grade'),
url(r'^student/', views.students, name='student'),
]
```



#### __init__.py文件 配置pymysql

`import pymysql`

`pymysql.install_as_MySQLdb()`

#### 配置静态资源

```
#静态资源配置
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'

#跳转登录页面
#该设置作用是用户不登录将没法访问网页
LOGIN_URL = '/user/login/'
```



####url反向解析

`src = '/app/left/'`

`src = "{% url 'namespace:name' %}"`

`src = "{% url 'app:left' %}"`

####静态解析两种方式

`<img src='/statc/img/xxx.css>'`

{% load static %}
`<img src='{% static "img/xxx.css" %}'>`

####过滤器 '|'

```
lower

upper

date:Y-m-d   h:i:s

add:1  

add:-1

```



#### 过滤url

```127.0.0.1:8080/app/api/student/?s_name=王&sex=1```

模糊查询

```Student.objects.all().filter(delete=False).filter(s_name__contains=王)```

```
#查询python班下语文成绩比数学成绩多10分以上的学生
    grade = Grade.objects.filter(g_name='python').first()
    stus = grade.student_set.all()

    stu = stus.filter(s_yuwen__gte=F('s_shuxue') + 10)

#查询python班语文大于等于80或者数学小于等于80的学生

    student = stus.filter(Q(s_yuwen__gte=80) | Q(s_shuxue__lte=80))
#查询python班语文小于80并且数学小于等于80的学生
    student = stus.filter(~Q(s_yuwen__gte=80) & Q(s_shuxue__lte=80))
```





####get和filter区别

get一定要确定能获取到唯一一个对象
filter：能获取很多对象，queryset

```first():```获取第一个
```[:1]```
```last()：```获取最后一个

####分页

paginator对象

```page_range：```获取当前一共有多少页 range(1,3)


page对象：

通过page获取paginator对象：page.paginator

```pages.has_next:```是否有下一页
```pages.has_previous：```是否有上一页
```pages.next_page_number：```下一页的页码
```pages.previous_page_number：```上一页的页码

```pages.number: ```当前页

```pages.paginator.page_range: ```获取总的页数

例子：

```
def grade(request):
    """班级"""
    if request.method == 'GET':
    	page_num = request.GET.get('page_num', 1)  #返回str类型  默认开始在第一页 获取请求页
        
    	grades = Grade.objects.all()
    	paginator = Paginator(grades, 3)#这里定义三个班级占一页
    	pages = paginator.page(int(page_num)) #得到指定页数里面的班级对象
     	return render(request, 'grade.html', {'grades': grades, 'pages': pages})
```

```
</div>

<ul id="PageNum">
<li><a href="{% url 'app:grade' %}">首页</a></li>
    {% if pages.has_previous %}
        <li><a href="{% url 'app:grade' %}?page_num={{ pages.previous_page_number }}">上一页</a></li>
    {% endif %}

    {% for i in pages.paginator.page_range %}
        <li><a href="{% url 'app:grade' %}?page_num={{ i }}">{{ i }}</a></li>
    {% endfor %}
    {% if pages.has_next %}
        <li><a href="{% url 'app:grade' %}?page_num={{ pages.next_page_number }}">下一页</a></li>
    {% endif %}
<li>当前是第{{ pages.number }}页</li>


<li><a href="{% url 'app:grade' %}?page_num={{ pages.paginator.num_pages }}">尾页</a></li>
</ul>

</div>
```

### 头像

settings.py文件设置：

```
#该设置是为导入头像
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

models.py设置

```
class Student(models.Model):
    s_name = models.CharField(max_length=20, null=False, unique=True)
    s_create_time = models.DateTimeField(auto_now_add=True)#时间不能更改
    s_operate_time = models.DateTimeField(auto_now=True)#时间会随着表格改动更新
    
    # 把头像存入upload文件中
    s_img = models.ImageField(upload_to='upload', null=True)
    
    g = models.ForeignKey(Grade)
    s_shuxue = models.IntegerField(null=True)
    s_yuwen = models.IntegerField(null=True)
    delete = models.BooleanField(default=False)#是否被删除
```

项目下的urls.py文件设置:

```
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
```

添加学生(包含头像)

```
def addstu(request):
    if request.method == 'GET':
        grades = Grade.objects.all()
        return render(request, 'addstu.html', {'grades': grades})

    if request.method == 'POST':
        s_name = request.POST.get('s_name')
        g_id = request.POST.get('g_id')
        
        #获取学生头像图片
        s_img = request.FILES.get('s_img')
        
        #获取学生的班级信息
        grade = Grade.objects.filter(id=g_id).first()#得到列表里面的元素
        #创建学生信息
        Student.objects.create(s_name=s_name, g=grade, s_img=s_img)
        return HttpResponseRedirect(reverse('app:student'))
```

html文件:

```
<th>头像</th>
    <td>
        <div class="txtbox floatL" style="width: 150px;">
            <input type="file" name="s_img">
        </div>
    </td>
```



###用户注册、登录、注销

##### 1. 系统自带模块auth实现

先进行注册，如果输入的信息无误则将信息传入后台

`User.objects.create(username=username, password=password)`

注册好了重定向到登录页面

然后验证登录用下面的方式



```
user=auth.authenticate(username=username, password=password)
if user:
	auth.login(request, user) #如果user正确则进行登录
	return HttpResponseRedirect(reverse('app:index')) #重定向到首页
else:
	msg = '用户名或密码错误'
	return render(request, 'login.html', {'msg': msg})
```



如果验证的返回值为真， 则重定向到网站首页

###### 注销：

```
def djlogout(request):
    """注销"""
	if request.method == 'GET':
		auth.logout(request)
		return HttpResponseRedirect(reverse('user:login'))
```



##### 2. 自定义实现

###### 注册跟上面一样(可以用make_password()函数对密码进行加密)

###### 登录：

```
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        user = Users.objects.filter(username=username).first()
        if user:
        	if check_password(password, user.password):#验证输入的密码是否正确
            #先产生随机的字符串，长度28
            	s = 'ddssjddhdshdjajshdshaqwertyu'
            	ticket = ''
            	for _ in range(28):

		    		ticket += random.choice(s) #登录的时候产生ticket值,注册的时候没有
			   response = HttpResponseRedirect(reverse('app:index'))
             	out_time = datetime.now() + timedelta(days=14) #过期期限是14天
             	response.set_cookie('ticket', ticket, expires=out_time)#expires表示cookie的有效期限

                #2.保存ticket在服务器后台
                User.objects.create(user=user, out_time=out_time, ticket=ticket)


                return response

            else:
                msg2 = '密码错误'
                return render(request, 'login.html', {'msg2': msg2})
        else:
            msg3 = '用户不存在'
            return render(request, 'login.html', {'msg3': msg3})

```

##### 验证登录有两种方式：

1.中间件

setting设置:

应用名.文件名.类名

文件里面的类从MiddlewareMixin继承过来

```
class UserAuthMiddle(MiddlewareMixin):

    def process_request(self, request):
        #验证cookie中的ticket，验证不通过，跳转到登录页面
        #验证通过，request.user代表当前登录的用户信息
        #return None 或者不写return

        path = request.path
        s = ['/user/login/', '/user/register/']
        if path in s:
            return None
        ticket = request.COOKIES.get('ticket')

        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))

        user = Users.objects.filter(ticket=ticket).first()#筛选得到cookie里的ticket与服务器里的ticket相同的用户
        if user:
        #获取到有认证的相关信息,out_time是user的属性，表示过期时间
        #1.验证当前认证信息是否过期，如果没过期，request.user赋值
        #2.如果过期了，跳转到登录，并删除认证信息
        	if datetime.utcnow() > user.out_time.replace(tzinfo=None):
        #datetime.utcnow()与user.out_time类型不同不能进行比较，必须user.out_time把tzinfo设为None它们才是相同的类型
                #  过期了
                user.delete()
                return HttpResponseRedirect(reverse('user:login'))
			else:
                #没有过期，把当前用户赋给request.user, 并且删除多余的认证信息
                request.user = user
                #删除多余的认证信息，也就是说把之前登录时保留下来的老的ticket删除，最后服务器只保留最新的ticket

    			User.objects.filter(Q(id=user.id)&~Q(ticket=ticket)).delete()
    			return None
		else:
         	return HttpResponseRedirect(reverse('user:login'))
        


```



2.装饰器

```
def is_login(func):
    def check_login(request):
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))

        user = Users.objects.filter(ticket=ticket)
        if not user:
            return HttpResponseRedirect(reverse('user:login'))
        return func(request)
    return check_login
```



###### 注销

```
def logout(request):
    if request.method == 'GET':
        request.user.ticket = None  #删除服务器里的ticket值
        request.user.save()
        response = HttpResponseRedirect(reverse('user:login'))

        response.delete_cookie('ticket') #注销后浏览器cookie里的ticket也会删除

        return response
```



##rest风格

1. 资源, 统一接口， 状态转移

```127.0.0.1:8080/app/student/：```获取所有的学生 GET

```127.0.0.1:8080/app/student/: ```创建的学生 POST


```127.0.0.1:8080/app/student/1/: ```获取学生中id为1的那一个学生 GET

```127.0.0.1:8080/app/student/1/: PUT、PATCH```

```127.0.0.1:8080/app/student/1/: DELETE```


```127.0.0.1:8080/app/grade/：```获取所有的班级 GET

2. http请求方式

GET：用于获取
POST： 用于创建
PUT：用于修改， 全部属性都会修改
PATCH: 用于修改，部分属性进行修改
DELETE: 删除

3. 旧接口

```127.0.0.1:8080/app/student/?id=1```

```127.0.0.1:8080/app/student/1/```



4. 安装filter包和rest包

```
pip install django_filter

pip install djangorestframework==3.4.6
```



5. ```to_representation中instance```是当前循环的学生的对象

   

#### 符合rest framework 的API接口

1. ###### setting设置

```
REST_FRAMEWORK = {
    
    'DEFAULT_PAGINATION_LCASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,  #分页配置, 可以得到一个分页的接口
    'DEFAULT_AUTHENTICATION_CLASSES': (),# 该设置的作用是不用它默认的用户认证方式，这样才可以自定义用户认证
    'DEFAULT_RENDERER_CLASSES': 'utils.functions.CustomJsonRenderer', #作用是渲染json数据格式，如果用该风格写接口的话这个步骤就非常重要

    #配置过滤
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter'),
}
```

2. ###### url设置

```
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'^api/student', views.api_student)
urlpatterns += router.urls

```

3. ###### 对象的序列化

```
from rest_framework import serializers

from app.models import Student, Grade

#对象的序列化操作
class StudentSerializer(serializers.ModelSerializer):

    s_name = serializers.CharField(max_length=20, error_messages={
        'blank': '姓名字段不能为空'
    })

    class Meta:
        model = Student
        fields = ['id', 's_name', 's_yuwen', 'g', 's_img']

    def to_representation(self, instance): #instance 即实例对象
        data = super().to_representation(instance)  #这里是一个一个的取出学生信息的，而不是一次性显示全部学生，返回完一个之后再回到这里取出第二个
        data['g_name'] = instance.g.g_name
        return data


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ['id', 'g_name']

    def do_update(self, instance, validated_data):
        instance.g_name = validated_data['g_name']
        instance.save()

        data = self.to_representation(instance)
        data['code'] = 300
        data['msg'] = '修改班级信息成功'
        return data


```

4. ###### 对象的过滤

```
import django_filters
from rest_framework import filters

from app.models import Student


class StudentFilter(filters.FilterSet):
	#模糊查询学生s_name姓名
    s_name = django_filters.CharFilter('s_name', lookup_expr='contains')
    #查询语文成绩大于s_yuwen_min 并且小于s_yuwen_max
    s_yuwen_min = django_filters.NumberFilter('s_yuwen', lookup_expr='gte')
    s_yuwen_max = django_filters.NumberFilter('s_yuwen', lookup_expr='lte')

    class Meta:
        model = Student
        fields = ['s_name']

```

5. 重写JSONRenderer下的render函数渲染数据格式

   ```
   from rest_framework.renderers import JSONRenderer
   class CustomJsonRenderer(JSONRenderer):
       """修改code和msg的结果"""
       '''
       {
       'data':{result},
       'code': 200,
       'msg': '请求成功',
       }
   
       '''
       def render(self, data, accepted_media_type=None, renderer_context=None):
           if renderer_context: #如果有响应，返回了信息
               if isinstance(data, dict):
                   code = data.pop('code', 0)
                   msg = data.pop('msg', '请求成功')
               else:
                   code = 0
                   msg = '请求成功'
   
               res = {
                   'code': code,
                   'msg': msg,
                   'data': data
               }
               return super().render(res, accepted_media_type, renderer_context)
           else:
               return super().render(data, accepted_media_type, renderer_context)
   
   ```

   

   

6. view逻辑、删除信息

```
from rest_framework import mixins, viewsets


class  api_student(mixins.ListModelMixin,  #对应的get请求
                   mixins.UpdateModelMixin, #对应的put, patch
                   mixins.CreateModelMixin,  #对应的post
                   mixins.DestroyModelMixin,  #对应的delete
                   viewsets.GenericViewSet):
    #查询学生的所有信息
    queryset = Student.objects.all().filter(delete=False)
    #序列化学生的所有信息
    serializer_class = StudentSerializer
    #过滤学生
    filter_class = StudentFilter

#重写删除方法， 删除页面上的，不删除数据库的内容
 def perform_destroy(self, instance):
    instance.delete = True
    instance.save()
    
 （def destroy(self, request, *args, **kwargs):

    instance = self.get_object()

    self.perform_destroy(instance)

    return Response(status=status.HTTP_204_NO_CONTENT)
）这是在做删除操作调用perform_destroy时的底层实现过程   
```

7. ajax请求

```
$.get(url, function(msg){
})



$.post(url, function(msg){

})



以上方式:url表示请求的地址，function(msg)代表，请求成功后的回调函数，msg是api返回的结果

$.ajax({

	url:'', # 请求的url地址，

	type:'', # GET POST PATCH PUT DELETE

	data：{'name':name,'sex':sex}，  # 代表请求的参数

	dataType:'json',

	headers:{'X-CSRFToken': csrf}  # 代表传递的csrf值

	success:function(msg){

		成功执行回调函数
	},

	error:function(msg){

		失败执行回调函数

	}

});

```



友情链接：github[仓库地址](https://github.com/coco369/knowledge)

