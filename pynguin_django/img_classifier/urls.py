from django.conf.urls import url
from django.views.static import serve

from img_classifier import views
from pynguin_django import settings

urlpatterns = [
    url(r'^upload$', views.upload_file, name='upload_file'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]