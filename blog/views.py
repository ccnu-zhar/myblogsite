from django.shortcuts import render_to_response ,get_object_or_404, render
from .models import Blog,BlogType
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from read_statistics.utils import read_statistics_once_read
from comment.forms import CommentForm

def blog_list(request):

    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list,5)  #每10篇分页
    page_num = request.GET.get('page',1)  # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前代码
    # 获取页码范围
    page_range = list(range(max(current_page_num-3,1),current_page_num))\
                 +list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))

    # 省略标记
    if page_range[0] -1 >=2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')

    # 首页和尾页
    if page_range[0] !=1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    # 获取时间   order='DESC' 排序
    context['blogs_dates'] = Blog.objects.dates('create_time','month',order='DESC')

    return render(request,'blog_list.html',context)

# pk 组件
def blog_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list,5)  #每10篇分页
    page_num = request.GET.get('page',1)  # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前代码
    # 获取页码范围
    page_range = list(range(max(current_page_num-3,1),current_page_num))\
                 +list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))

    # 页码省略标记
    if page_range[0] -1 >=2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')

    # 首页和尾页
    if page_range[0] !=1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context = {}
    context['blog_type'] = blog_type
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range




    return render(request,'blog_with_type.html',context)

def blog_with_date(request,year , month):
    context = {}
    blogs_all_list = Blog.objects.filter(create_time__year = year,create_time__month = month )
    paginator = Paginator(blogs_all_list, 5)  # 每10篇分页
    page_num = request.GET.get('page', 1)  # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前代码
    # 获取页码范围
    page_range = list(range(max(current_page_num - 3, 1), current_page_num)) \
                 + list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 页码省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_with_date'] = '%s年%s月' %(year,month)
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blogs_dates'] = Blog.objects.dates('create_time', 'month', order='DESC')

    return render(request,'blogs_with_date.html', context)

def blog_detail(request,blog_pk):

    blog = get_object_or_404(Blog,pk = blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    conmments = Comment.objects.filter(content_type = blog_content_type, object_id = blog.pk)
    context = {}
    # 当前博客的上一篇
    context['previous_blog']  = Blog.objects.filter(create_time__gt =blog.create_time).last()
    # 当前博客的下一篇 filter得到的是一个集合   .first()  .last()选择第一个  、 最后一个
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()

    context['blog'] = blog
    context['comments'] = conmments
    data = {}
    data['content_type'] = blog_content_type.model
    data['object_id'] = blog_pk
    context['comment_form'] = CommentForm(initial=data)
    # render的返回值默认有user
    response = render(request,'blog_detail.html',context) # 响应
    response.set_cookie(read_cookie_key,'true')
    return response




# 分页之前blog_with_type
# def blog_with_type(request, blog_type_pk):
#     context = {}
#     blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
#
#     context['blog_types'] = BlogType.objects.all()
#     context['blogs'] = Blog.objects.filter(blog_type=blog_type)
#     context['blog_type'] = blog_type
#
#     return render(request,'blog_with_type.html', context)

