# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from .models import Post, Comment
from .forms import PostForm, EmailPostForm, CommentForm
#from django.core.paginator import PageNotAnInteger, EmptyPage , Paginator






def base(request):
    title  = 'blog'
    return render(request, 'Myblog/base.html', {'title':title})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'Myblog/list.html'
    paginate_by = 2

def addpost(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()

            return HttpResponseRedirect('/Myblog/list')

    else:
        post_form = PostForm()
    return render(request, 'Myblog/addpost.html',{'post_form':post_form, })





def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug = slug, publish__year = year, publish__month = month, publish__day = day)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()



    return render(request, 'Myblog/detail.html', {'post':post, 'comments':comments, 'comment_form':comment_form})


def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            post_url = request.build_absolute_uri(post.get_absolute_url())
            data = form.cleaned_data
            subject = '{} from email id {} recommends you to read {}'.format(data['name'], data['email'], data['comment'])
            message = '{} {} for this post this is comment:{}'.format(post.title, post_url, data['comment'])
            send_mail(subject,message, 'hrishabhpatidar1996@gmail.com' ,[data['to']], fail_silently=False)
            sent =True
    else:
        form = EmailPostForm()
    return render(request, 'Myblog/share.html', {'form':form, 'posts':post, 'sent':sent})


