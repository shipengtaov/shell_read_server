# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from posts.models import Category, Post


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def post(request):
    if request.method == 'GET':
        username = request.GET.get("username", "").strip()
        category_name = request.GET.get("category", "").strip()
        # 随机获取
        # see: https://stackoverflow.com/questions/962619/how-to-pull-a-random-record-using-djangos-orm
        # 检查 category 是否存在
        # category_exist = Category.objects.filter(name=category_name)
        # if category_exist:
        #     category = Category(name=category_name)
        #     posts = Post.objects.filter(category=category, created_at>=)
        return JsonResponse(dict(success=True, data=["hi"
            ]))

    elif request.method == 'POST':
        username = request.POST.get('username', settings.DEFAULT_USERNAME).strip()
        category_name = request.POST.get('category', settings.DEFAULT_CATEGORY_NAME).strip()
        content = request.POST.get('content', '').strip()
        img_url = request.POST.get('img_url', '').strip()

        if not username or not category_name or not content:
            return JsonResponse(dict(success=False, msg=u'信息不完整'))
        if len(username) > settings.USERNAME_MAX_LENGTH:
            return JsonResponse(dict(
                    success=False,
                    msg=u'用户名最长为 %d 个字符' % settings.USERNAME_MAX_LENGTH))
        if len(category_name) > settings.CATEGORY_MAX_LENGTH:
            return JsonResponse(dict(
                    success=False,
                    msg=u'类别名最长为 %d 个字符' % settings.CATEGORY_MAX_LENGTH))
        if len(content) > settings.POST_MAX_LENGTH:
            return JsonResponse(dict(
                    success=False,
                    msg=u'post 最多 %d 个字符' % settings.POST_MAX_LENGTH))

        category_exist = Category.objects.filter(name=category_name).exists()
        if category_exist:
            category = Category.objects.filter(name=category_name).get()
            category.post_count = F('post_count') + 1
        else:
            category = Category(name=category_name, post_count=1)
        category.save()

        post = Post(username=username, content=content, img_url=img_url,
                    category=category)
        post.save()
        return JsonResponse(dict(success=True))
