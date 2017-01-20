"""
All URLs for the Rango project are to be routed here.
"""
from django.conf.urls import url
from rango import views

urlpatterns = [
                  url('^$', views.index, name="index"),
                  url(r'^about/$', views.about, name="about")
              ]
