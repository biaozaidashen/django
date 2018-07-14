from json import dumps

from django import forms
from django.http import HttpResponse
from django.shortcuts import render
import pymysql

from hrs.models import Dept, Emp


def index(request):
    ctx = {
        'greeting': '你好, 世界'
    }
    return render(request, 'index.html', context=ctx)


def depts(request):
    ctx = {'dept_list': Dept.objects.all}
    return render(request, 'dept.html', context=ctx)


def emps(request, no='0'):
    #no = request.GET['dno']
    emps_list = list(Emp.objects.filter(dept__dno=no).select_related('dept'))
    # dept = Dept.objects.get(pk=no)
    # emps_list = dept.emps.all()
    ctx = {
        #'emps_list': emps_list, 'dept_name': dept.name
        'emps_list': emps_list, 'dept_name': emps_list[0].dept.name
    }if len(emps_list) > 0 else {}
    # if emps_list.count() > 0 else {}
    return render(request, 'emp.html', ctx)


def deldept(request, no='0'):
    try:
        Dept.objects.get(pk=no).delete()
        ctx = {'code': 200}
    except:
        ctx = {'code': 404}
    return HttpResponse(
        dumps(ctx),
        content_type='application/json; charset=utf-8')
    # 重定向--重新请求一个指定页面
    #第一种return depts(request)
    #第二种方法：return redirect(reverse('depts'))
    #第三种方法：
    # ctx = {
    #     'dept_list': Dept.objects.all()
    # }
    # return render(request, 'dept.html', ctx)


class DeptForm(forms.Form):
    dno = forms.IntegerField(label='部门编号')
    name = forms.CharField(max_length=20, label='部门名称')
    location = forms.CharField(max_length=10, label='部门所在地')


def add(request):
    errors = []
    if request.method == 'GET':
        f = DeptForm()
    else:
        f = DeptForm(request.POST)
        if f.is_valid():
            Dept(**f.cleaned_data).save()
            f = DeptForm()
        else:
            errors = f.errors.values()
    return render(request, 'add.html', {'f': f, 'errors': errors})