from django.shortcuts import render_to_response,get_object_or_404
from blog.models import *
# Create your views here.


def blog_list(request):
    blogs = Blog.objects.all()
    return render_to_response('blog/blog_list.html', locals())


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog/blog_detail.html', locals())


def blogs_with_type(request, blogs_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blogs_type_pk)
    blogs = Blog.objects.filter(blog_type=blog_type)
    return render_to_response('blog/blogs_with_type.html', locals())
