import random

from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = {"code":1008,"msg":"无权访问！"}

    def has_permission(self, request, view):
        #获取请求中的数据，然后进行校验

        v1 = random.randint(1,3)
        if v1 == 1 or v1== 2:
            print("p1")
            return True
        return False


class MyPermission2(BasePermission):
    message = {"code":1008,"msg":"无权访问！"}

    def has_permission(self, request, view):
        #获取请求中的数据，然后进行校验

        v1 = random.randint(1,3)
        if  v1 == 1 or v1== 2:
            print("p2")
            return True
        return False

class MyPermission3(BasePermission):
    message = {"code":1008,"msg":"无权访问！"}

    def has_permission(self, request, view):
        #获取请求中的数据，然后进行校验

        v1 = random.randint(1,3)
        if  v1 == 1 or v1== 2:
            print("p3")
            return True
        return False


class UserPermission(BasePermission):
    message = {"code":1008,"msg":"无权访问！"}

    def has_permission(self, request, view):
        #获取请求中的数据，然后进行校验
        if request.user.role == 3: ##注意1.drf中是先认证，认证成功后，在权限验证，2.认证时返回的二元组对应request.user和request.auth 去看看认证返回了什么东西
            return True
        return False

class ManagerPermission(BasePermission):
    message = {"code":1008,"msg":"无权访问！"}

    def has_permission(self, request, view):
        #获取请求中的数据，然后进行校验
        if request.user.role == 2:
            return True
        return False

class BossPermission(BasePermission):
    message = {"code":1008,"msg":"无权访问！"}

    def has_permission(self, request, view):
        #获取请求中的数据，然后进行校验
        if request.user.role == 1:
            return True
        return False