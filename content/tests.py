from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from content.models import EmailContent, LanguageContent, MediaContent
from content.factories import MediaContentFactory


class EmailContentModelTest(TestCase):

    def test_email_content_exists(self):
        entry = EmailContent(
            subject='Test',
            content_type=EmailContent.SHARE_LINK,
            language_code='en',
            text='Link {link}', html='<a href="{link}">Link</div>')
        entry.save()

        self.assertEqual(str(entry), entry.subject)

    def test_email_content_duplicate(self):
        """
        EmailContent has foreign content together on type & language_code
        """
        with self.assertRaises(IntegrityError):
            EmailContent(
                subject='Test',
                content_type=EmailContent.SHARE_LINK,
                language_code='en',
                text='Link {link}',
                html='<a href="{link}">Link</div>').save()

            EmailContent(
                subject='Test',
                content_type=EmailContent.SHARE_LINK,
                language_code='en',
                text='Link {link}',
                html='<a href="{link}">Link</div>').save()


class LanguageContentModelTest(TestCase):

    def test_language_content_exists(self):
        entry = LanguageContent(
            language_code='en',
            content_type='ui',
            content='{"test": "test"}')
        entry.save()

        self.assertEqual(str(entry), '{content_type}, {language_code}'.format(
            content_type=entry.content_type,
            language_code=entry.language_code))

    def test_language_content_duplicate(self):
        """
        LanguageContent has the unique on the language_code field
        """
        with self.assertRaises(IntegrityError):
            LanguageContent(
                language_code='en',
                content_type='ui',
                content="{'test': 'test'}").save()

            LanguageContent(
                language_code='en',
                content_type='ui',
                content="{'test': 'test'}").save()


class MediaContentModelTest(TestCase):

    def test_media_content_exists(self):
        media_content = MediaContentFactory()
        # If id more than 0, the mean is the data is already saved
        self.assertTrue(media_content.id > 0)


class ShareLinkViewTest(TestCase):

    def test_share_link_ok(self):
        client = APIClient()

        # To send a share link, we need an email content
        EmailContent(
            content_type=EmailContent.SHARE_LINK,
            language_code='en',
            subject='Share link',
            text='{link}',
            html='<div>{link}</div>').save()

        response = client.post(
            path='/content/share-link/',
            data={
                'email': 'taufik@zimmermanzimmerman.nl',
                'language_code': 'en',
                'link': 'https://www.sample.com'
            },
            format='json',
            **{'REMOTE_HOST': 'localhost:3000'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_link_forbidden(self):
        """
        Test the status forbidden because the remote host
        is not registered on the settings.py
        """
        client = APIClient()

        # To send a share link, we need an email content
        EmailContent(
            content_type=EmailContent.SHARE_LINK,
            language_code='en',
            subject='Share link',
            text='{link}',
            html='<div>{link}</div>').save()

        response = client.post(
            path='/content/share-link/',
            data={
                'email': 'taufik@zimmermanzimmerman.nl',
                'language_code': 'en',
                'link': 'https://www.sample.com'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LanguageContentViewTest(TestCase):

    def test_language_content_ok(self):
        client = APIClient()

        LanguageContent(
            language_code='en',
            content_type='ui',
            content="{'test': 'test'}").save()

        # Because the permission class is protected by remote host,
        # we set REMOTE_HOST value to allowed host.
        response = client.get(
            path='/content/language-content/en/ui/',
            data=None,
            follow=False,
            **{'REMOTE_HOST': 'localhost:3000'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MediaContentViewTest(TestCase):

    def test_media_content_ok(self):
        # Check if the endpoint of the current media content is working.
        client = APIClient()
        media_content = MediaContentFactory()
        url = reverse(
            'content:api-media-content', kwargs={'slug': media_content.slug})
        response = client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





