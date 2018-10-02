from django.conf.urls import url
from content import views

app_name = 'content'
urlpatterns = [
    url(r'^share-link/$',
        views.ShareLinkView.as_view(), name='api-share-link'),
    url(r'^language-content/(?P<language_code>[\w-]+)/'
        r'(?P<content_type>[\w-]+)/$',
        views.LanguageContentView.as_view(), name='api-language-content'),
    url(r'^media-content/(?P<slug>[\w-]+)/$',
        views.MediaContentView.as_view(), name='api-media-content'),
]
