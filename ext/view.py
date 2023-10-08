#将 APIView 源码中 权限的校验改为 逻辑或的校验
from rest_framework.views import APIView

# 类似于bootstrap 新建一个类，继承

class NBAPIView(APIView):

    def check_permissions(self, request):
        no_permission_objects = []
        for permission in self.get_permissions():
            if  permission.has_permission(request, self):
               return
            else:
                no_permission_objects.append(permission)

        self.permission_denied(
                    request,
                    message=getattr(no_permission_objects[0], 'message', None),
                    code=getattr(no_permission_objects[0], 'code', None)
                )