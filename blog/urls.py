from django.conf.urls import url

from . import views
app_name='blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),
    url(r'^search/$',views.search,name='search'),
    url(r'^blog_list/$',views.blog_list,name='blog_list'),
    url(r'^about/$',views.about,name='about'),
    url(r'^pray/$',views.pray,name="pray"),
    url(r'^cha/$',views.cha,name='cha'),
    url(r'^cha_prize/$',views.get_cha,name='get_prize'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.tag, name='tag')
]
