from django.db import models
from django.contrib.auth.models import User

# 导入富文本编辑
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=30)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    # content = models.TextField()
    # 导入富文本编辑
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete = models.DO_NOTHING)

    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    '''    ## 补充的  不知道什么意思
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readnum = None
'''


    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        ordering = ['-create_time']
'''
class ReadNum(models.Model):
    # 阅读计数
    read_num = models.IntegerField(default=0)
    # ForeignKey 一对多 OneToOneField 一对一
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
'''