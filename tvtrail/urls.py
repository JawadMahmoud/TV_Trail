from django.conf.urls import url
from tvtrail import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^series/(?P<tv_show_slug>[\w\-]+)/$', 
        views.show_tvseries, name='show_tvseries'),
]