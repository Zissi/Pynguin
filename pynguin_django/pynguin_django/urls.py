from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pynguin_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^img_classifier/', include('img_classifier.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
