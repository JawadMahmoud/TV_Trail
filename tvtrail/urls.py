from django.conf.urls import url
from tvtrail import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^series/(?P<tv_show_slug>[\w\-]+)/(?P<username>[\w\-]+)/$', 
        views.show_tvseries, name='show_tvseries'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
]