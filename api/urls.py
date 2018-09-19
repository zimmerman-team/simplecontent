from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^share-link/$',
        views.ShareLinkView.as_view(), name='api-share-link'),
    url(r'^language-content/(?P<language_code>[\w-]+)/(?P<type>[\w-]+)/$',
        views.LanguageContentView.as_view(), name='api-language-content'),
]
