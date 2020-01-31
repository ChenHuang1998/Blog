from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=32)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)

    def __str__(self):
        return '<Blog:%s>' % self.title


