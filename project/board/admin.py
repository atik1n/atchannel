from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Post, Category, Board, Thread

admin.site.register(Category)
admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(Post)
