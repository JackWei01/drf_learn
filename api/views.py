import uuid
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import models
from ext.auth import MyAuthentication,MyAuthentication2
from ext.code import ERROR_CODE
from ext.permission import UserPermission,ManagerPermission,BossPermission
from ext.throttle import MyThrottle,IPThrottle,UserThrottle
from ext.view import NBAPIView


# Create your views here.
def home(request): #因为没有继承   drf 的 APIView,所以全局配置的认证不影响这个view
    return HttpResponse("success!")


class UserView(APIView):
    #业务需求，此时视图标配是查看用户信息，需要登录，前端携带token
    #经理  总监  用户 都可以访问

    # def get(self,request,*args,**kwargs): #两种写法都行
    def get(self,request):#两种写法都行

        print(request.user,request.auth)

        return Response("OK")

    def post(self,request):
        print(request.user, request.auth)

        return Response("OK")

# class UserView(APIView):
#     # def get(self,request,*args,**kwargs): #两种写法都行
#     def get(self,request,id,name):#两种写法都行
#
#         print(id,name)
#
#         print(self.args)
#         print(self.kwargs)
#
#         print(self.kwargs.get("id"))
#         print(self.kwargs.get("name"))
#
#         print(request.user)
#         print(request.auth)
#
#         print(request.method)
#         print(request.data)
#
#         return Response("OK")

class apilistview(APIView):
    #需要认证
    authentication_classes = [MyAuthentication,MyAuthentication2] #默认情况下，如果多个认证类都没有认证成功或者认证失败，
    # 都return none,drf默认是以匿名用户的方式(self.user,self.auth=None)执行view，如果要改动则需要自定义最后一个认证类时，手动return
    def get(self,request):
        print(request.user)
        print(request.auth)
        return Response("api list:\n1.index\n2.get_dirs")

class loginview(APIView):
    #，用户登录界面，不需要认证,不需要权限
    authentication_classes = [] #全局+局部，会局部优先，，取消全局的设定
    # permission_classes = [BossPermission, ManagerPermission, UserPermission] #同上，不走全局的权限校验
    throttle_classes = [IPThrottle]
    def get(self,request):
        return Response("username:?password:?")

    def post(self,request):
        # 1.接受用户提交的用户名密码
        #方法1
        # print(request.body)
        # print(request._request.body)
        #方法2
        print(request.data) #获取bodu的数据，直接是个字典类型
        print(request.query_params) #获得url的数据

        username = request.data.get("username")
        password =  request.data.get("password")


        # 2.数据库校验
        user_obj =  models.UserInfo.objects.filter(username=username,password=password).first()

        if not user_obj:
            # return  Response({"code":1001,"msg":"用户名或密码错误"}) #其中code 是项目中自行商量定义的
            return  Response({"code":ERROR_CODE,"msg":"用户名或密码错误"}) #其中code 是项目中自行商量定义的

        #3,用户名密码正确，生成token  返回并写入数据库
        token = str(uuid.uuid4())

        user_obj.token = token
        user_obj.save()

        return Response({"status":True,'data':token})


    # return Response("username:?password:? Failed")

class OrderView(NBAPIView): #NBAPIView,改写了原理APIView中的权限校验的策略，之前的策略是其中一个不满足就失败，全部满足才满足，而自定义修改过后权限类之间是逻辑或的关系
    #总监，经理可以访问，但是员工不能访问
    # authentication_classes = []

    # permission_classes = [MyPermission,]
    permission_classes = [BossPermission, ManagerPermission]
    throttle_classes = [UserThrottle,IPThrottle]

    def get(self,request):
        print(request.user,request.auth)
        # return Response("Orderview")
        self.dispatch
        return Response({"code":10006,"data":[11,22,33,44]})

    # def check_permissions(self, request):
    #     no_permission_objects = []
    #     for permission in self.get_permissions():
    #         if permission.has_permission(request, self):
    #             return
    #         else:
    #             no_permission_objects.append(permission)
    #
    #     self.permission_denied(
    #         request,
    #         message=getattr(no_permission_objects[0], 'message', None),
    #         code=getattr(no_permission_objects[0], 'code', None)
    #     )


class AvatarView(NBAPIView):
    #经理 和 员工可以看
    permission_classes = [ManagerPermission, UserPermission] #注意源码中的多个权限是与的关系，任意一个不满足，则权限校验不通过
    def get(self,request):
        return Response("AvatarView")


