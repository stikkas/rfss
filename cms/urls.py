from django.conf.urls import patterns, url


urlpatterns = patterns('cms.views.home',
    url(r'^$', 'home', name='home'),
)

urlpatterns += patterns('cms.views.profile',
    url(r'^user/(?P<user_pk>\d+)/$', 'profile', name='profile'),
    url(r'^user/(?P<user_pk>\d+)/edit/$', 'edit_profile', name='edit_profile'),
)

# Metrika
urlpatterns += patterns('cms.views.metrika',
    url(r'^metrika/$', 'statistic', name='statistic'),

    url(r'^metrika/traffic/$', 'traffic', name='stat_traffic'),
    url(r'^metrika/traffic/(?P<date1>\d+)/(?P<date2>\d+)/$', 'traffic',
        name='stat_traffic'),

    url(r'^metrika/traffic/hourly/$', 'traffic_hourly',
        name='stat_traffic_hourly'),
    url(r'^metrika/traffic/hourly/(?P<date1>\d+)/(?P<date2>\d+)/$',
        'traffic_hourly', name='stat_traffic_hourly'),

    url(r'^metrika/sources/$', 'sources', name='stat_sources'),
    url(r'^metrika/sources/(?P<date1>\d+)/(?P<date2>\d+)/$', 'sources',
        name='stat_sources'),

    url(r'^metrika/browsers/$', 'browsers', name='stat_browsers'),
    url(r'^metrika/browsers/(?P<date1>\d+)/(?P<date2>\d+)/$', 'browsers',
        name='stat_browsers'),

    url(r'^metrika/countries/$', 'countries', name='stat_countries'),
    url(r'^metrika/countries/(?P<date1>\d+)/(?P<date2>\d+)/$', 'countries',
        name='stat_countries'),

    url(r'^metrika/regions/$', 'regions', name='stat_regions'),
    url(r'^metrika/regions/(?P<date1>\d+)/(?P<date2>\d+)/$', 'regions',
        name='stat_regions'),
)

# Messenger
urlpatterns += patterns('cms.views.messenger',
    url(r'^messenger/write/$', 'write_message', name='write_message'),
    url(r'^messenger/sentbox/$', 'sentbox', name='sentbox'),
    url(r'^messenger/sentbox/message/(?P<pk>\d+)/detail/$',
        'sentbox_message', name='sentbox_message'),
    url(r'^messenger/sentbox/message/(?P<pk>\d+)/delete/$',
        'delete_sentbox_message', name='delete_sentbox_message'),
    url(r'^messenger/inbox/$', 'inbox', name='inbox'),
    url(r'^messenger/inbox/message/(?P<pk>\d+)/detail/$',
        'inbox_message', name='inbox_message'),
    url(r'^messenger/inbox/message/(?P<reply_mesg_pk>\d+)/reply/$',
        'write_message', name='reply_inbox_message'),
    url(r'^messenger/inbox/message/(?P<pk>\d+)/delete/$',
        'delete_inbox_message', name='delete_inbox_message'),
)

urlpatterns += patterns('cms.views.menu',
    url(r'^menu/(?P<pk>\d+)/$', 'menu', name='menu'),
    url(r'^menu/$', 'menu', name='menu'),
)

urlpatterns += patterns('cms.views.auth',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)

# Pages component
urlpatterns += patterns('cms.views.pages',
    url(r'^menu/(?P<menu_pk>\d+)/add/page/$', 'page_add', name='page_add'),
    url(r'^page/(?P<pk>\d+)/edit/$', 'page_edit', name='page_edit'),
    url(r'^page/(?P<pk>\d+)/delete/$', 'page_delete', name='page_delete'),
    url(r'^attachment/(?P<pk>\d+)/download/$', 'get_attach', name='get_attach'),
    url(r'^attachment/(?P<pk>\d+)/delete/$', 'attach_delete', name='attach_delete'),
)

urlpatterns += patterns('cms.views.search',
    url(r'^search/$', 'search', name='search'),
)

urlpatterns += patterns('cms.views.moderate',
    url(r'^moderate/pages/$', 'moderate_pages', name='moderate_pages'),
    url(r'^moderate/page/(?P<page_pk>\d+)/$', 'moderate_page', name='moderate_page'),
    url(r'^moderate/page/(?P<page_pk>\d+)/publish/$',
        'moderate_page_publish', name='moderate_page_publish'),
    url(r'^moderate/page/(?P<page_pk>\d+)/unpublish/$',
        'moderate_page_unpublish', name='moderate_page_unpublish'),
    url(r'^moderate/page/(?P<page_pk>\d+)/comment/$',
        'moderate_write_comment', name='moderate_write_comment'),

    url(r'^moderate/new_users/$', 'moderate_new_users', name='moderate_new_users'),
    url(r'^moderate/new_user/(?P<pk>\d+)/confirm/$',
        'moderate_new_user_confirm', name='moderate_new_user_confirm'),
    url(r'^moderate/new_user/(?P<pk>\d+)/reject/$',
        'moderate_new_user_reject', name='moderate_new_user_reject'),

    url(r'^moderate/comments/$', 'moderate_comments', name='moderate_comments'),
    url(r'^moderate/comment/(?P<pk>\d+)/publish/$',
        'moderate_comment_publish', name='moderate_comment_publish'),
    url(r'^moderate/comment/(?P<pk>\d+)/delete/$',
        'moderate_comment_delete', name='moderate_comment_delete'),
)

# Person component
urlpatterns += patterns('cms.views.person',
    url(r'^menu/(?P<menu_pk>\d+)/add/person/$', 'person_add', name='person_add'),
    url(r'^person/(?P<pk>\d+)/edit/$', 'person_edit', name='person_edit'),
    url(r'^person/(?P<pk>\d+)/delete/$', 'person_delete', name='person_delete'),
)

# Help
urlpatterns += patterns('cms.views.help',
    url(r'^help/(?P<tmpl_name>\S+)/$', 'help', name='help'),
)

