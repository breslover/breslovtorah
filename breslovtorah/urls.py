from django.conf.urls import patterns, include, url
from django.contrib import admin 
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'breslovtorah.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index.html$', 'breslovtorah.frontpage.views.home', name='home'),
    url(r'^sefer/(?P<slug>.*).html$', 'breslovtorah.frontpage.views.sefer', name='sefer'),
    url(r'^$', RedirectView.as_view(url='index.html', permanent=True), name='index')
)
