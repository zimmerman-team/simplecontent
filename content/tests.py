import mock

from django.test import TestCase
from django.core.files import File
from django.db.utils import IntegrityError

from content.models import EmailContent, LanguageContent


class EmailContentTest(TestCase):

    def test_email_content_exists(self):
        entry = EmailContent(
            subject='Test',
            type=EmailContent.SHARE_LINK,
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
                type=EmailContent.SHARE_LINK,
                language_code='en',
                text='Link {link}',
                html='<a href="{link}">Link</div>').save()

            EmailContent(
                subject='Test',
                type=EmailContent.SHARE_LINK,
                language_code='en',
                text='Link {link}',
                html='<a href="{link}">Link</div>').save()


class LanguageContentTest(TestCase):

    def test_language_content_exists(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'file_mock.json'

        entry = LanguageContent(
            language_code='en',
            json_file=file_mock)
        entry.save()

        self.assertEqual(str(entry), entry.language_code)

    def test_language_content_duplicate(self):
        """
        LanguageContent has the unique on the language_code field
        """
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'file_mock.json'

        with self.assertRaises(IntegrityError):
            LanguageContent(
                language_code='en',
                json_file=file_mock).save()

            LanguageContent(
                language_code='en',
                json_file=file_mock).save()

    def test_should_the_same_filename(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'file_mock.json'

        entry = LanguageContent(
            language_code='en',
            json_file=file_mock)
        entry.save()

        entry.json_file = file_mock
        entry.save()

        folder_filename = '{folder}/{filename}'.format(
            folder='language-content', filename=file_mock.name)

        self.assertEqual(entry.json_file.name, folder_filename)
