from django.conf.urls import patterns, include, url
from django.contrib import admin 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'breslovtorah.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index.html$', 'breslovtorah.frontpage.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
