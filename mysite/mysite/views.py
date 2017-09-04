from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # 分页
from blogs.models import Blog, Label
# Create your views here.

def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    page = request.GET.get('page')
    try:
        blogs_list = paginator.page(page)
    except PageNotAnInteger :
        blogs_list = paginator.page(1)
    except EmptyPage:
        blogs_list = paginator.paginator(paginator.num_pages)

    return render(request, 'index.html', {'blogs_list' : blogs_list})