from django.contrib import admin
from .models import *


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    inlines = [PostCategoryInLine]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [PostCategoryInLine]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)