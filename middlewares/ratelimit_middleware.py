# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    """频率限制
    """
    def process_request(self, request):
        # ip = request.META['REMOTE_ADDR']
        pass
