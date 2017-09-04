from django.shortcuts import render


from blogs.models import Blog, Label
# Create your views here.

def home(request):
    blogs_list = Blog.objects.all()
    return render(request, 'index.html', {'blogs_list' : blogs_list})