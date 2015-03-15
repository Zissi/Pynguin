from django.conf.urls import patterns, url

from img_classifier import views
from pynguin_django import settings

urlpatterns = patterns('',
    url(r'^upload$', views.upload_file, name='upload_file'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)