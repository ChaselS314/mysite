from django.db import models

# Create your models here.


class Label(models.Model):
    '''
    name,blogs
    '''
    name = models.CharField(max_length=50)
    blogs = models.ManyToManyField(Blog)

    def __str__(self):
        return self.name


class Blog(models.Model):
    '''
    title,author,publication_date,labels,content
    '''
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publication_date = models.DateField()
    labels = models.ManyToManyField(Label)
    content = models.TextField()

    def __str__(self):
        return self.title