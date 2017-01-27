"""
All URLs for the Rango project are to be routed here.
"""
from django.conf.urls import url
from rango import views

urlpatterns = [url('^$', views.index, name="index"),
               url(r'^about/$', views.about, name="about"),
               url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name="add_page"),
               url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.view_category, name="view_category"),
               url(r'^add_category/$', views.add_category, name="add_category"),
               ]
