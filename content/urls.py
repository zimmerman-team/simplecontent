from django.conf.urls import url
from content import views

urlpatterns = [
    url(r'^share-link/$',
        views.ShareLinkView.as_view(), name='api-share-link'),
    url(r'^language-content/(?P<language_code>[\w-]+)/'
        r'(?P<content_type>[\w-]+)/$',
        views.LanguageContentView.as_view(), name='api-language-content'),
]
