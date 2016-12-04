# -*- coding: utf-8 -*-

from django.http import HttpResponse


def handler404(request):
    return HttpResponse("404 not found")


def handler500(request):
    return HttpResponse("500 server error")
