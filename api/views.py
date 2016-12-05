# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from redis import StrictRedis

from posts.models import Category, Post
from posts import utils

redis_con = StrictRedis(**settings.REDIS)


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def post_view(request):
    cache_key = settings.RANDOM_POSTS_KEY
    cache_count = redis_con.scard(cache_key)

    if request.method == 'GET':
        nickname = request.GET.get("nickname", "").strip()
        category_name = request.GET.get("category", "").strip()

        # save cache
        if cache_count <= 0:
            print 'caching...'
            db_posts = Post.objects.filter(
                                deleted=False,
                                created_at__gte=utils.min_created_at()).all()
            for p in db_posts:
                redis_con.sadd(cache_key, p.pk)
            redis_con.expire(cache_key, settings.RANDOM_POSTS_EXPIRE)

        post_id = redis_con.srandmember(cache_key)

        # there is no any data
        if not post_id:
            return JsonResponse(dict(success=True, data=None))

        post = Post.objects.filter(id=post_id).get()
        read_count = post.read_count + 1
        post.read_count = F("read_count") + 1
        post.save()

        return JsonResponse(dict(success=True, data={
                "nickname": post.nickname,
                "content": post.content,
                "category": post.category.name,
                "read_count": read_count,
                "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }))

    elif request.method == 'POST':
        nickname = request.POST.get('nickname',
                                    settings.DEFAULT_NICKNAME).strip()
        category_name = request.POST.get(
                            'category',
                            settings.DEFAULT_CATEGORY_NAME).strip()
        content = request.POST.get('content', '').strip()
        img_url = request.POST.get('img_url', '').strip()

        if not nickname or not category_name or not content:
            return JsonResponse(dict(success=False, msg=u'信息不完整'))
        if len(nickname) > settings.NICKNAME_MAX_LENGTH:
            return JsonResponse(dict(
                    success=False,
                    msg=u'用户名最长为 %d 个字符' % settings.NICKNAME_MAX_LENGTH))
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

        post = Post(nickname=nickname, content=content, img_url=img_url,
                    category=category)
        post.save()
        # save to cache
        if cache_count > 0:
            redis_con.sadd(cache_key, post.pk)

        return JsonResponse(dict(success=True))
