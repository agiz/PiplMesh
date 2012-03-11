from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from piplmesh.frontend import views as frontend_views

# import social-auth views
from account.views import home, done, logout, error, form

urlpatterns = patterns('',
    url('^$', frontend_views.HomeView.as_view(), name='home'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # lazy signup registration
    url(r'^accounts/convert/', include('lazysignup.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'redirect_field_name': 'redirect_to',}, name='logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'redirect_field_name': 'redirect_to',}, name='login'),

    # social-auth login
    url(r'^form/$', form, name='form'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'', include('social_auth.urls')),
)