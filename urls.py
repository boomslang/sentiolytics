from django.conf.urls.defaults import patterns, include, url

from settings import STATIC_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sentio.views.home', name='home'),
    # url(r'^sentio/', include('sentio.foo.urls')),

    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^test/$', 'sentio.sentiolytics.views.test'),
    (r'^ajax_test/$', 'sentio.sentiolytics.views.my_ajax_view'),
    (r'^gcharts_test/$', 'sentio.sentiolytics.views.gcharts'),
    (r'^load_players/$', 'sentio.sentiolytics.views.load_players'),
    (r'^ajax_update_chart/$', 'sentio.sentiolytics.views.update_chart'),
#    (r'^map/$', 'sentio.sentiolytics.views.leaflet_view'),

    ################
    ################
    url(r'^$', 'sentio.sentiolytics.views.test'), # Should be the last element.
)
