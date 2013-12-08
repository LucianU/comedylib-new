"""
Global project URLs
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin

from search.forms import WildcardSearchForm
from search.views import GroupedResultsSearchView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^a52/', include(admin.site.urls)),
    url(r'^a/', include('accounts.urls')),
    url(r'^u/', include('profiles.urls')),
    url(r'^c/', include('django.contrib.comments.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^search/', GroupedResultsSearchView(form_class=WildcardSearchForm),
        name='haystack_search'),
    url(r'^com/', include('affiliates.urls', namespace='affiliates')),
    url(r'^', include('content.urls', namespace='content')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
