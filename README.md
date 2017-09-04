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