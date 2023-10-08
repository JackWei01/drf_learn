from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import models


class MyAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = request.query_params.get("token") #取不到token 这个元素是 request.query_params.get("token") 返回None

        if token == None:
            return

        if token == "wuhuqifei":
            return "wuhu",token #返回一个元祖，分别对应 request.user 和 request.auth

        # raise AuthenticationFailed({"code":402,"detial":"认证失败"}) #认证失败，源码中返回的是401，但实际代码返回的是HTTP 403 Forbidden
        return

    def authenticate_header(self, request): #响应状态码 #
        # return  "API"
        return  'Basic realm="API"'  #网页弹框，要求进行身份验证


class MyAuthentication2(BaseAuthentication):

    def authenticate(self, request):

        token = request.query_params.get("token")
        if token == "hanjinlong":
            return "jinlkong",token #返回一个元祖，分别对应 request.user 和 request.auth

        # raise AuthenticationFailed({"code":401,"detial":"认证失败"})
        return


class UrlAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = request.query_params.get("token")
        if token == "hanjinlong":
            return "jinlkong",token #返回一个元祖，分别对应 request.user 和 request.auth

        raise AuthenticationFailed({"code":401,"detial":"认证失败"})



class HeadAuthentication(BaseAuthentication): #请求头中获取token

    def authenticate(self, request):
        #假设前端以参数的形式携带token

        #接受token并比对
        token = request.META.get("HTTP_AUTHORIZATION")

        if token == None:
            return

        user_obj = models.UserInfo.objects.filter(token=token).first()

        if user_obj: #存在token对应的
            return user_obj,token # 此时 request.user = user_obj.request.auth = token

        return

    def authenticate_header(self, request):
        return "API"

        # if token == "hanjinlong":
        #     return "jinlkong",token #返回一个元祖，分别对应 request.user 和 request.auth

        # raise AuthenticationFailed({"code":20000,"detial":"认证失败"})


class QueryParamsAuthentication(BaseAuthentication): #get ?

    def authenticate(self, request):
        #假设前端以参数的形式携带token

        #接受token并比对
        token = request.query_params.get("token")

        if token == None:
            return

        user_obj = models.UserInfo.objects.filter(token=token).first()

        if user_obj: #存在token对应的
            return user_obj,token # 此时 request.user = user_obj.request.auth = token

        return

    def authenticate_header(self, request):
        return "API"
        # if token == "hanjinlong":
        #     return "jinlkong",token #返回一个元祖，分别对应 request.user 和 request.auth

        # raise AuthenticationFailed({"code":20000,"detial":"认证失败"})




class BodyAuthentication(BaseAuthentication):  #请求体中获取

    def authenticate(self, request):

        token = request.query_params.get("token")
        if token == "hanjinlong":
            return "jinlkong",token #返回一个元祖，分别对应 request.user 和 request.auth

        raise AuthenticationFailed({"code":401,"detial":"认证失败"})


class AnonymousDeny(BodyAuthentication):

    def authenticate(self, request):

        raise AuthenticationFailed({"code":10002,"detial":"认证失败"})

    def authenticate_header(self, request):
        return "API"