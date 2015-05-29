from django.conf.urls import url, patterns

urlpatterns = patterns('cms.tests.url_builders.views',
    url(r'^check_link/$', 'check_link', name='check_link'),
    url(r'link/(?P<pk>\d+)/', 'link', name='link')
)

