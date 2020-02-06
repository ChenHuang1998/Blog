from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField
from read_statistics.models import ReadNumExpandMethod,ReadDetail
# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=32)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=128)
    content = MDTextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)

    def __str__(self):
        return '<Blog:%s>' % self.title

    class Meta:
        ordering = ['-created_time']


