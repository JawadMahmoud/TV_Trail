from django.conf.urls import url
from tvtrail import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^series/(?P<tv_show_slug>[\w\-]+)/$', 
        views.show_tvseries, name='show_tvseries'),
    url(r'^series_follow/(?P<tv_show_slug>[\w\-]+)/$', 
        views.series_follow, name='series_follow'),
    url(r'^episode/(?P<tv_show_slug>[\w\-]+)/(?P<season_param>[\w\-]+)/(?P<episode_param>[\w\-]+)/$', 
        views.show_episode, name='show_episode'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^explore/(?P<alphabet>[\w\-]+)/$', views.explore_alpha, name='explore_alpha'),
    url(r'^explore/', views.explore, name='explore'),
]