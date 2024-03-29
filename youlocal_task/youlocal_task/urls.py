from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from website import urls as website_urls


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'youlocal_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'', include(website_urls)),
)
