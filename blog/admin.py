from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'image', 'views_counter', 'create_at']
    list_filter = ('title', 'views_counter', 'create_at')
    search_fields = ('title', 'create_at')
