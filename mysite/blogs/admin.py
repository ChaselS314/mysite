from django.contrib import admin

# Register your models here.
from .models import Blog, Label

admin.site.register(Blog)
admin.site.register(Label)
