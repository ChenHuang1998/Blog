from django.contrib import admin
from comment.models import *
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'text', 'comment_time', 'user')