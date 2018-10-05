from django.conf.urls import url
from content import views

app_name = 'content'
urlpatterns = [
    url(r'^share-link/$',
        views.ShareLinkView.as_view(), name='api-share-link'),
    url(r'^media/(?P<slug>[\w-]+)/$',
        views.MediaContentView.as_view(), name='api-media-content'),
    url(r'^json/(?P<slug>[\w-]+)/$',
        views.JSONContentView.as_view(), name='api-json-content'),
]
