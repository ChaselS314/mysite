from django.shortcuts import render
from django.http import Http404
# Create your views here.
from .models import Blog

def detail(request, id):
    try:
        blog = Blog.objects.get(id=str(id))
    except Blog.DoesNotExist:
        raise Http404
    return render(request, 'blogs/blog.html', {'blog':blog})