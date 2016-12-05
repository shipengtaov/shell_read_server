# -*- coding: utf-8 -*-

from django.db import models


class Category(models.Model):
    """类别
    """
    name = models.CharField(unique=True, max_length=30,
                            blank=False, null=False)
    post_count = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Post(models.Model):
    """Post
    """
    nickname = models.CharField(max_length=30, null=False)
    content = models.TextField(blank=False, null=False)
    img_url = models.CharField(max_length=500, blank=True, null=False)
    category = models.ForeignKey(Category)
    # 读次数
    read_count = models.IntegerField(default=0)
    # 是否已删除
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.category.name + ' : ' + self.content[:10]
