from rest_framework import status
from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache as default_cache
from django.utils.translation import gettext_lazy as _
class MyThrottle(SimpleRateThrottle):
    scope = "v1"
    # THROTTLE_RATES = {'v1':'5/m'}  #此处不写就会到settings中的 "DEFAULT_THROTTLE_RATES":{"v1":"5/m", "v2":"10/m", "v3":"10/s"} 找 "v1"对应的速度

    cache = default_cache


    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk #获得一登陆用户ID
        else: #用户未登录 此时的  request.user 为 None
            ident = self.get_ident(request)#

        return self.cache_format % {'scope':self.scope,'ident':ident}

class IPThrottle(SimpleRateThrottle):
    #修改返回的节流信息
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _('请求受限！')
    extra_detail_singular = _('请等待{wait}秒后，再访问！')
    extra_detail_plural = _('请等待{wait}秒后，再访问！')
    default_code = 'throttled'


    scope = "ip"
    # THROTTLE_RATES = {'v1':'5/m'}  #此处不写就会到settings中的 "DEFAULT_THROTTLE_RATES":{"v1":"5/m", "v2":"10/m", "v3":"10/s"} 找 "v1"对应的速度

    cache = default_cache

    def get_cache_key(self, request, view):

        ident = self.get_ident(request)  #

        return self.cache_format % {'scope': self.scope, 'ident': ident}


class UserThrottle(SimpleRateThrottle):

    #修改返回的节流信息
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _('请求受限！')
    extra_detail_singular = _('请等待{wait}秒后，再访问！')
    extra_detail_plural = _('请等待{wait}秒后，再访问！')
    default_code = 'throttled'

    scope = "user"
    # THROTTLE_RATES = {'v1':'5/m'}  #此处不写就会到settings中的 "DEFAULT_THROTTLE_RATES":{"v1":"5/m", "v2":"10/m", "v3":"10/s"} 找 "v1"对应的速度

    cache = default_cache

    def get_cache_key(self, request, view):

        ident = request.user.pk  # 获得一登陆用户ID


        return self.cache_format % {'scope': self.scope, 'ident': ident}
