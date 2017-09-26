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

## Day 6

> 至此，基本的网站框架完成。接下来开始准备将网站放在到互联网上。

> refer : [Deploying Django to production](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment)

### 总览

- 对工程的设置做一些调整
- 选择一个托管(hosting)Django app的环境
- 选择一个托管静态文件的环境
- 设置产品级的基础架构，为自己的网站提供服务

### 选择托管服务提供商

我选择的是[Heroku](https://www.heroku.com/)

> 原因：免费，支持Django。以后需要的话可能会改。可以参考refer进行选择。

### 修改网站设置

为了安全及性能原因，需要对`settings.py`进行修改：

- `DEBUG`.在产品中，应该将其设置为`Fasle`
- `SECRET_KEY`.这是一串很长的随机值用于**CRSF**保护。在真正发布的产品中，要注意保护它的隐私性。千万不要随着git发布到github里: )

修改`settings.py`:

```python
...
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag'
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')
...
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )
...
```

### 为Heroku做准备

#### Heroku如何工作

> In order to execute your application Heroku needs to be able to set up the appropriate environment and dependencies, and also understand how it is launched. For Django apps we provide this information in a number of text files:
>
> - **runtime.txt**:** **the programming language and version to use.
> - **requirements.txt**: the Python component dependencies, including Django.
> - **Procfile**: A list of processes to be executed to start the web application. For Django this will usually be the Gunicorn web application server (with a `.wsgi` script).
> - **wsgi.py**: [WSGI](http://wsgi.readthedocs.io/en/latest/what.html) configuration to call our Django application in the Heroku environment.

#### 创建一个Git仓库

Heroku与git版本控制系统高度集成，可以通过git的上传/同步等操作将本地的改变即时应用到网站上。

git的创建不赘述，但请注意两点:

- 记得添加`.gitignore`文件。
- 在`manage.py`所在的目录创建仓库，或者在其它地方新建仓库，将 `manage.py`所在目录的所有文件及目录复制过去。

Tips: 使用Github的`.gitigonre`模板，过滤*python*的一些"垃圾"文件。

在`.gitignore`中增加:

```shell
# Text backup files
*.bak

#Database
*.sqlite3
```

#### 为Heroku更新Django app

##### Procfile

在git仓库的根目录创建`Procfile`，添加下行:

```shell
web: gunicorn locallibrary.wsgi --log-file -
```

> The "`web:`" tells Heroku that this is a web dyno and can be sent HTTP traffic. The process to start in this dyno is *gunicorn*, which is a popular web application server that Heruko recommends. We start Gunicorn using the configuration information in the module `locallibrary.wsgi` (created with our application skeleton: **/locallibrary/wsgi.py**).

##### Gunicorn

[Gunicorn](http://gunicorn.org/)是Heroku推荐的HTTP服务器提供商。

虽然不需要其在本地做什么，但还是安装一下以便接下来设置开发环境:

```shell
pip install gunicorn
```

##### 数据库配置

Heroku不支持SQLite。Heroku使用数据库插件来完成数据库的功能。

- 安装`dj-database-url`: `pip install dj-database-url`
- 在`settings.py`中添加:

```python
# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
```

- psycopg2 (Python Postgres database support),但我们不需要在本地配置它，只需手动加到`requirements.txt`.

##### 保存静态文件

需要配置`settings.py`中的变量`STATIC_ROOT`和`STATIC_URL`

其实，我们之前已经配置过了，嗯。。[官方说明](https://docs.djangoproject.com/en/1.10/howto/static-files/)

##### Whitenoise

> There are many ways to serve static files in production. Heroku recommends using the [WhiteNoise](https://warehouse.python.org/project/whitenoise/) project for serving of static assets directly from Gunicorn in production.

- 安装WhiteNoise : `pip install whitenoise`
- 在`settings.py`的`MIDDLEWARE`中增加:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

- (可选)，在`settings.py`增加一下代码，用于缩小静态文件的大小来使网站更高效(添加到最后即可):

```python
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

##### Requirements

- 使用`pip freeze > requirements.txt`生成requirements.txt
- 检查生成的文件，至少应该包含以下几项(版本可能不同)，请删除除此之外的其他项，除非你确定你在你的app中使用了它(比如我就使用了Markdown)。

```shell
dj-database-url==0.4.1
Django==1.10.2
gunicorn==19.6.0
psycopg2==2.6.2
whitenoise==3.2.2
```

> 确保`psycopg2`在你的requirements.txt，没有的话，请加上。

##### Runtime

增加`runtime.txt`,它会告诉Heroku使用的是哪一种编程语言。在其中添加以下:

```shell
python-3.6.2
```

> **Note:** Heroku only supports a small number of [Python runtimes](https://devcenter.heroku.com/articles/python-support#supported-python-runtimes). You can specify other Python 3 runtime values, but at time of writing the above version will actually be supported for definite.

#### 保存更改

保存以上更改，并提交到git。

在本地测试，确定网站没有被我们改坏: )

### 创建Heroku账户并安装

- 在[官网](https://www.heroku.com/)注册账号
- 根据[指导](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)安装CLI到本地
- 创建并上传网站

```shell
heroku create
git push heroku master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

- 打开网站！:

```shell
heroku open
```

> 这个时候可能打开是错误，因为没有把当前域名添加到允许的host列表里。

### 配置环境变量

#### 检查环境变量:

`heroku config`

#### 设置`DJANGO_SECRET_KEY`：

`heroku config:set DJANGO_SECRET_KEY=your_secret_key`

#### 设置`DJANGO_DEBUG`：

`heroku config:set DJANGO_DEBUG=''`

#### 设置`ALLOWED_HOSTS`:

```python
ALLOWED_HOSTS = ['<your app URL without the https:// prefix>.herokuapp.com',]
```

#### 保存并提交

```shell
git add -A
git commit -m 'Update ALLOWED_HOSTS with site and development server URL'
git push heroku master
```

### 发布完成！

## Day 7 使用自己的域名

### 购买域名

我是在[godaddy](https://ca.godaddy.com/)上买的。

### 配置Heroku使用自己的域名

> Refer: [Custom Domain Names for Apps](https://devcenter.heroku.com/articles/custom-domains)

#### 认识概念：

- **domain** or **domain name**: full name used to access an app (in words, not with an IP address). For example, `www.yourcustomdomain.com`
- **subdomain**: the `www` in `www.yourcustomdomain.com`
- **root domain** (or naked, bare, or zone apex domain): the 'yourcustomdomain.com’ in 'www.yourcustomdomain.com’
- **wildcard domain**: domains that match any subdomain, represented as `*.yourcustomdomain.com`
- **Domain registration service**: company that lets your buy and register a custom domain name
- **DNS provider**: company that maintains the DNS servers that translate a custom domain name to a destination ('DNS Target’). The fields are often called CNAME, ALIAS, ANAME, or A records. Only the first three work with Heroku apps, as A records require an IP address and Heroku apps do not have stable inbound IP addresses.
- **Heroku Domain**: Heroku term for default domain given to each app. Has the form `[name of app].herokuapp.com`
- **DNS Target**: Heroku term for the Heroku Domain to give to a DNS Provider (e.g., in a CNAME record) to be the destination for a custom domain name.

#### 查看当前域名

```shell
heroku domains
```

#### 使用subdomain定制自己的网站

```shell
$ heroku domains:add www.example.com
Adding www.example.com to ⬢ example-app... done
 ▸    Configure your app's DNS provider to point to the DNS Target
 ▸    www.example.com.herokudns.com.
 ▸    For help, see https://devcenter.heroku.com/articles/custom-domains

The domain www.example.com has been enqueued for addition
 ▸    Run heroku domains:wait 'www.example.com' to wait for completion
```

##### 为subdomains配置DNS

- 打开Godaddy，个人页面，manage Domains，manage DNS
- 删除所有默认的`CNAME`
- 增加`CNAME`,`www`,`www.example.com.herokudns.com`
- 使用`host`命令查看DNS是否已经转移，这需要一段时间。出现以下信息说明已经完成:

```shell
$ host www.example.com
www.example.com is an alias for www.example.com.herokudns.com.
...
```

#### 配置root domain

- 打开Godaddy，个人页面，manage Domains，use your domain
- connect to existing website,填写上一步配置好的subdomain

### 完成。

## Day 8
### Code Highlighting
网上有很多code highlighting的js代码，这是我用的[highlight.js](https://highlightjs.org/)
- 在`base.html`中增加代码:
```html
...
<link rel="stylesheet"
      href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/github.min.css">
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
...
```
- *style*可以自己修改，可选类型在网站上都有。

## Day 9

### Debug Error 500

现在的网站存在一个问题: 当DEBUG = Fasle时，访问网站会出现 ERROR 500。
查找了很多资料，发现问题的原因主要有(不限于)一下三种:
- 没有将域名加入到ALLOWED_HOSTS中，低级错误，我不属于这种: )
- static文件路径配置错误，导致一些static文件发生import错误。配置的方法参考[官网说明](https://docs.djangoproject.com/en/1.11/howto/static-files/) ，很遗憾我也不属于这种
- 使用了`whitenoise`的压缩方法配置了`STATICFILES_STORAGE`，导致了错误，找不到需要的static文件。
> 解决方法：注释掉类似于`STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`的代码即可。我属于这种，摸不着头脑。

在查找问题时发现了一个tips：DEBUG模式下，Django会在控制台输出log信息，可以方便的定位问题。但是在非DEBUG模式下，控制台不输出任何信息，这个时候很难定位问题。

> 解决方法：在`settings.py`中加入以下代码:
>
> ```python
> LOGGING = {
>     'version': 1,
>     'disable_existing_loggers': False,
>     'formatters': {
>         'verbose': {
>             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
>             'datefmt' : "%d/%b/%Y %H:%M:%S"
>         },
>         'simple': {
>             'format': '%(levelname)s %(message)s'
>         },
>     },
>     'handlers': {
>         'file': {
>             'level': 'DEBUG',
>             'class': 'logging.FileHandler',
>             'filename': 'mysite.log',
>             'formatter': 'verbose'
>         },
>     },
>     'loggers': {
>         'django': {
>             'handlers':['file'],
>             'propagate': True,
>             'level':'DEBUG',
>         },
>         'MYAPP': {
>             'handlers': ['file'],
>             'level': 'DEBUG',
>         },
>     }
> }
> ```
>
> 这会将log信息输出到指定文件中`mysite.log`。


