

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class PublishManger(models.Manager):
    def get_queryset(self):
        return super(PublishManger,self).get_queryset().filter(status = 'published')

class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_posts',default='1')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    published = PublishManger() #custom manager

    def get_absolute_url(self):
        return reverse('Myblog:post_detail', args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])


    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=50)
    post = models.ForeignKey(Post, related_name= 'comments')
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default =True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} commnet this {}'.format(self.name, self.post)



