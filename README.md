# mysite
## Day 1
### 创建project 
```shell
django-admin startproject mysite
python manage.py migrate
python manage.py runserver
```
### 创建主页
- 在根目录新建文件夹`templates`,并在其中创建`index.html`,随便写点`hello,world`
- 在`mysite/mysite`目录中新建`views.py`，创建显示主页的类`views.home`
- 在`urls.py`中，增加到`views.home`的正则匹配
- 这个时候就可以在主页显示`hello,world`了
- 在Pure上找主页模板，根据需要选择[博客模板](https://purecss.io/layouts/),下载该模板，
其中包含index.html和一些CSS和image。
- 将模板index.html替换掉原来的index.html，但这个时候会提示css等**not found**
- 通过[官方文档](https://docs.djangoproject.com/en/1.11/howto/static-files/)了解到，CSS等`static file`，需要特殊处理，类似`templates`。
- 在根目录创建`static`文件夹，将模板中的css和img文件夹拷贝到其中；在`settings.py`中，增加定义`STATICFILES_DIR=[os.path.join(BASE_DIR, 'static'),]`;在`index.html`中，增加`{% load static %}`,并将指向css和img的链接加上`static`声明。详见[文档](https://docs.djangoproject.com/en/1.11/howto/static-files/)
- 这个时候就可以显示出和Pure展示的一样的效果了
- 新增`base.html`，将基础框架从`index.html`抽离出来。
## Day 2
### 创建Model : blogs
```shell
python manage.py startapp blogs
```
### 创建管理员账户
```shell
python manage.py createsuperuser
```
### 完善Model
- 定义类Blog和Label，多对多的关系
## Day 3
### 测试Model
在python django shell中测试model : (不知道如何在命令行给外键赋值)
or:
在admin.py中注册两个模型，通过admin网页添加数据做测试
- 在admin.py中：
```python
from .models import Blog, Label

admin.site.register(Blog)
admin.site.register(Label)
```
- 在终端更新数据库:
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
- 登陆admin网页，添加测试数据
### 显示BLog
- 修改index.html如下:
```html
{% extends "base.html" %}

{% block content %}
<div class="blogs">
    {% for blog in blogs_list %}
        <section class="blog">
            <header class="blog-header">
                <h2 class="blog-title">{{ blog.title }}</h2>

                    <p class="blog-meta">
                        Time:  <a class="blog-author" href="#">{{ blog.publication_date }}</a>
                        {% for label in blog.labels.all %}
                        <a class="blog-category blog-category-js" href="#">{{ label }}</a>
                        {% endfor %} 
                    </p>
            </header>

                <div class="blog-description">
                    <p>
                        {{ blog.content }}
                    </p>
                </div>
        </section>
    {% endfor %}
</div><!-- /.blog-blog -->
{% endblock %}
```
- 重写views.home(),传入参数`blogs_list`
- 至此，可以在主页显示出测试数据了
### 使用动态URL，为每个blog创建单独的页面显示
- 更新mysite/urls.py:
```python
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^blog/', include('blogs.urls')),
]
```
- 更新blogs/urls.py
```python
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)/$', views.detail, name="detail"),
]
```
- 更新blogs/views.py
```python
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
```
- 新建blogs/templates/blog.html
```html
{% extends "base.html" %}

{% block content %}
<div class="blog">
    <section class="blog">
        <header class="blog-header">
            <h1 class="blog-title">{{ blog.title }}</h1>
                <p class="blog-meta">
                    Time:  <a class="blog-author" href="#">{{ blog.publication_date }}</a>
                    {% for label in blog.labels.all %}
                    <a class="blog-category blog-category-js" href="#">{{ label }}</a>
                    {% endfor %} 
                </p>
        </header>
        <div class="blog-description">
            <p>
                {{ blog.content }}
            </p>
        </div>
    </section>   
</div><!-- /.blog-blog -->
{% endblock %}
```
- 更新index.html,更新超链接:
```html
...
<h2 class="blog-title"><a href="{% url "detail" id=blog.id %}">{{ blog.title }}</a></h2>
...
```
- 至此，完成每个blog的单独页面显示
### 使博文显示支持Markdown格式
- 首先要安装python的markdown包，它可以将Markdown格式的文本转化为HTML文本
- 在blogs-app中新建`templatetags`文件夹，在其中添加`__init__.py`，使其成为一个包
- 在templatetags中添加custom_markdown.py：
```python
import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()  #自定义filter时必须加上


@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def custom_markdown(value):
    return mark_safe(markdown.markdown(value,
        extensions = ['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'],
        safe_mode=True, enable_attributes=False))
```
- 更新blog.html：
```html
...
{% load custom_markdown %}
...
{{ blog.content | custom_markdown }}
...
```
- 至此，文章单独显示的界面就可以支持Markdown格式了。
### 优化主页的显示效果
- 更新index.html:
```html
{{ blog.content | custom_markdown | truncatewords_html:30 }}
```
限制每篇blog在主页显示的长度。
- 更新index.html
```html
<p>
    <a href="{% url "detail" id=blog.id %}">查看全文</a>
</p>
```
增加**查看全文**链接。
- 更新base.html:
```html
...
 <a href="/">
    <img src={% static "img/monkey.png" %} width="90" height="100">
</a>
...
```
增加一个图像作为主题图像，并内置返回主页的链接。
### 增加分页功能
- 修改mysite/views.py:
```python
...
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # 分页
...
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
```
- 更新index.html:
```html
...
{% if blogs_list.object_list and blogs_list.paginator.num_pages > 1 %}
      <div>
      <ul class="pager">
      {% if blogs_list.has_previous %}
        <a href="?page={{ blogs_list.previous_page_number }}">上一页</a>
      {% endif %}

      {% if blogs_list.has_next %}
        <a href="?page={{ blogs_list.next_page_number }}">下一页</a>
      {% endif %}
      </ul>
      </div>
    {% endif %}
...
```
- 至此，增加了分页功能
## Day 4
### 优化主页标题栏的显示
修改`index.html`:
```html
...
<p class="blog-meta">
    <a href="#">{{ blog.author }}</a>
    <a class="blog-author" href="#">{{ blog.publication_date | date:"Y M d" }}</a>
    {% for label in blog.labels.all %}
    <a class="blog-category blog-category-js" href="#">{{ label }}</a>
    {% endfor %} 
</p>
...
```
增加作者的显示，并修改日期的显示格式
## Day 5
### 优化Markdown的显示效果
- 下载[github-markdown.css](https://github.com/sindresorhus/github-markdown-css)
- 将css文件保存在`static/css`目录下
- 修改`base.html`，按照[指导](https://github.com/sindresorhus/github-markdown-css)添加代码:
```html
...
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href={% static "css/github-markdown.css" %}>
<style>
    .markdown-body {
        box-sizing: border-box;
        min-width: 200px;
        max-width: 980px;
        margin: 0 auto;
        padding: 45px;
    }

    @media (max-width: 767px) {
        .markdown-body {
            padding: 15px;
        }
    }
</style>
...
```
- 继续修改`base.html`，在`block content`上添加css类的声明，表示我们期望在`block content`中使用css样式：
```html
...
<div class="content pure-u-1 pure-u-md-3-4">
        <div>
            <div class="markdown-body">
            {% block content %}
            {% endblock %}
            </div>
            <div class="footer">
                <div class="pure-menu pure-menu-horizontal">
...
```
- 这样，即可由`custom_markdown`将markdown文本转换为html文本，再通过css样式表将其在网页上合理的展示出来。