from django.contrib import admin

# Register your models here.
from src.blog.models import BlogPost

admin.site.register(BlogPost)