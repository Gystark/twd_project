"""
All URLs for the Rango project are to be routed here.
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rango import views

urlpatterns = [
                  url('^$', views.index, name="index"),
                  url(r'^about/$', views.about, name="about")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
