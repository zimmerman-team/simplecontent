from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^share-link/', views.ShareLink.as_view(), name='api-share-link'),
]
