from django.contrib import admin

from hrs.models import Dept, Emp

#调整后台显示
class DeptAdmin(admin.ModelAdmin):
    list_display = ('dno', 'name', 'location', 'excellent')
    ordering = ('dno', )#升序，  降序：-dno


class EmpAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'job', 'sal', 'dept')
    search_fields = ('name', 'job') #给员工在后台添加搜索功能
    ordering = ('dept', )


admin.site.register(Dept, DeptAdmin)
admin.site.register(Emp, EmpAdmin)
