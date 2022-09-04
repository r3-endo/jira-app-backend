# adminサイトで操作可能なモデル
from django.contrib import admin
# import
from .models import Category, Task, Profile

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Profile)