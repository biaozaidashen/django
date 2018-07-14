from django.urls import path
from django.conf.urls import url
from hrs import views

urlpatterns = [
    #命名捕获组
    #url('emps/(?P<no>[0-9]+)', views.emps, name='empsdd'), 这是django1的写法
    path('depts', views.depts, name='depts'),
    path('emps/<int:no>', views.emps, name='empsdd'),#这是django2版本写法
    path('deldept/<int:no>', views.deldept, name='ddel'),
]