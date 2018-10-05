from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from content.factories import (
    MediaContentFactory, JSONContentFactory, EmailContentShareLinkFactory
)


class ShareLinkTest(TestCase):

    def test_email_content_share_link_record_created(self):
        # Check if record created
        email_content = EmailContentShareLinkFactory()
        # If id more than 0, the mean is the data is already saved
        self.assertTrue(email_content.id > 0)

    def test_email_content_share_link_endpoint_ok(self):
        # Check if endpoint is OK
        # Before make request we need a record share link on Email Content
        EmailContentShareLinkFactory()
        # Test endpoint
        client = APIClient()
        url = reverse('content:api-share-link')
        response = client.post(
            path=url,
            data={
                'email': 'taufik@zimmermanzimmerman.nl',
                'link': 'https://www.sample.com'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MediaContentTest(TestCase):

    def test_media_content_record_created(self):
        # Check if created a record of the media content is working
        media_content = MediaContentFactory()
        # If id more than 0, the mean is the data is already saved
        self.assertTrue(media_content.id > 0)

    def test_media_content_endpoint_ok(self):
        # Check if the endpoint is OK of the current media content
        client = APIClient()
        media_content = MediaContentFactory()
        url = reverse(
            'content:api-media-content', kwargs={'slug': media_content.slug})
        response = client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JSONContentTest(TestCase):

    def test_json_content_record_created(self):
        # Check if create a record of the json content if working
        json_content = JSONContentFactory()
        # If id more than 0, the record is already created
        self.assertTrue(json_content.id > 0)

    def test_json_content_endpoint_ok(self):
        # Check if the endpoint is OK of the current JSON content
        client = APIClient()
        json_content = JSONContentFactory()
        url = reverse(
            'content:api-json-content', kwargs={'slug': json_content.slug})
        response = client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

