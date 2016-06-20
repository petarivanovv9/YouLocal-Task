from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import index, save_venues, get_venues_in_5km_desc


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'youlocal_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name='index'),
    url(r'^save/$', save_venues, name='save_venues'),

    url(r'^venues/$', get_venues_in_5km_desc),
)
