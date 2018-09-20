from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.files.base import ContentFile

from rest_framework.test import APIClient
from rest_framework import status

from content.models import EmailContent, LanguageContent, MediaContent


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


class ImageContentModelTest(TestCase):

    def test_image_content_exists(self):
        # hex encoded bytes of a tiny valid png file
        valid_png_hex = ['\x89', 'P', 'N', 'G', '\r', '\n', '\x1a', '\n',
                         '\x00',
                         '\x00', '\x00', '\r', 'I', 'H', 'D', 'R', '\x00',
                         '\x00', '\x00', '\x01', '\x00', '\x00', '\x00',
                         '\x01',
                         '\x08', '\x02', '\x00', '\x00', '\x00', '\x90',
                         'w', 'S', '\xde', '\x00', '\x00', '\x00', '\x06', 'b',
                         'K',
                         'G', 'D', '\x00', '\x00', '\x00', '\x00',
                         '\x00', '\x00', '\xf9', 'C', '\xbb', '\x7f', '\x00',
                         '\x00',
                         '\x00', '\t', 'p', 'H', 'Y', 's', '\x00',
                         '\x00', '\x0e', '\xc3', '\x00', '\x00', '\x0e',
                         '\xc3',
                         '\x01', '\xc7', 'o', '\xa8', 'd', '\x00', '\x00',
                         '\x00', '\x07', 't', 'I', 'M', 'E', '\x07', '\xe0',
                         '\x05',
                         '\r', '\x08', '%', '/', '\xad', '+', 'Z',
                         '\x89', '\x00', '\x00', '\x00', '\x0c', 'I', 'D', 'A',
                         'T',
                         '\x08', '\xd7', 'c', '\xf8', '\xff', '\xff',
                         '?', '\x00', '\x05', '\xfe', '\x02', '\xfe', '\xdc',
                         '\xcc',
                         'Y', '\xe7', '\x00', '\x00', '\x00', '\x00',
                         'I', 'E', 'N', 'D', '\xae', 'B', '`', '\x82']
        valid_png_bin = "".join(valid_png_hex)
        image_file = ContentFile(valid_png_bin)
        image_file.name = 'image_file.png'

        entry = MediaContent(content_type=MediaContent.HOME, image=image_file)
        entry.save()

        self.assertEqual(str(entry), '{content_type}, {image_name}'.format(
            content_type=entry.content_type, image_name=entry.image.name))


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
            path='/api/share-link/',
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
