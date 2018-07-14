from django.db import models


class Dept(models.Model):
    dno = models.IntegerField(primary_key=True, verbose_name='部门编号')
    name = models.CharField(max_length=20, verbose_name='部门名称')
    location = models.CharField(max_length=10, verbose_name='部门所在地')
    excellent = models.BooleanField(default=0, verbose_name='是否优秀')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_dept' #给表改名字


class Emp(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    job = models.CharField(max_length=10)
    mar = models.IntegerField(null=True, blank=True) #总裁的上司为空，
    sal = models.DecimalField(max_digits=7, decimal_places=2) #decimal_places意思是小数点后保留几位，max_digits是保留几位有效数字
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT, related_name='emps')  #ForeignKey一对多关系的外键

    class Meta:
        db_table = 'tb_Emp'



