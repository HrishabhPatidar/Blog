from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.base, name='Base'),
    url(r'^list/$', views.PostListView.as_view(), name= 'Post_list'),
    url(r'^addpost/$', views.addpost, name='Addpost'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',views.post_detail,name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),

]
