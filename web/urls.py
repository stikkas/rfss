from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Captcha
    url(r'^captcha/', include('captcha.urls')),
    # TinyMCE ImageManager connector
    url(r'^tinymce/image-manager/', include('tinymce.urls', namespace='tinymce')),
    # Django admin
    url(r'^admin/', include(admin.site.urls)),
    # CMS
    url(r'^manage/', include('cms.urls', namespace='cms')),
)

urlpatterns += patterns('web.views',
    url(r'^$', 'index', name='index'),
    url(r'^region/(?P<pk>\d+)/change/$', 'change_region', name='change_region'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^registration/$', 'registration', name='registration'),
    url(r'^search/$', 'search', name='search'),
    url(r'^menu/(?P<pk>\d+)/$', 'menu', name='menu'),
    url(r'^page/(?P<pk>\d+)/detail/$', 'page_detail', name='page_detail'),
    url(r'^page/comment/(?P<pk>\d+)/delete/$', 'page_comment_delete',
        name='page_comment_delete'),
    url(r'^polls/$', 'polls', name='polls'),
    url(r'^poll/(?P<pk>\d+)/$', 'poll', name='poll'),
    url(r'^poll/(?P<pk>\d+)/results/$', 'poll_results', name='poll_results'),
    url(r'^star_rating/(?P<pk>\d+)/vote/$', 'star_rating_vote', name='star_rating_vote'),
    url(r'^letters/$', 'letters', name='letters'),
    url(r'^letters/rules/$', 'letters_rules', name='letters_rules'),
    url(r'^letters/form/$', 'letters_form', name='letters_form'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
