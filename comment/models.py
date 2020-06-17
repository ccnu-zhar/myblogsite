from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Comment(models.Model):
    # 评论对象(博客)
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content__object = GenericForeignKey('content_type','object_id')
    # 评论内容
    text = models.TextField()
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 评论人
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-comment_time']
