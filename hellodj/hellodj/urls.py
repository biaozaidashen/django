
from django.contrib import admin
from django.urls import path, include
from hrs import views

#资源路径
urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    # path('hrs/depts', views.depts),
    # path('hrs/emps', views.emps),
    # path('hrs/deldept', views.deldept)
    path('hrs/', include('hrs.url')),#引用应用里面的路径
    path('add/', views.add)
]
