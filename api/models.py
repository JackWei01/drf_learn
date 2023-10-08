from django.db import models

# Create your models here.

class UserInfo(models.Model):
    '''
        用户表
    '''
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

    role = models.IntegerField(verbose_name="角色",choices=((1,'总监'),(2,'经理'),(3,'员工')),default=3)

    #临时方法 可以放到redis ,jwt中
    token = models.CharField(verbose_name="Token",max_length=64,null=True,blank=True)