from django.test import TestCase
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
        entry = LanguageContent(
            language_code='en',
            type='ui',
            content="{'test': 'test'}")
        entry.save()

        self.assertEqual(str(entry), '{type}, {language_code}'.format(
            type=entry.type, language_code=entry.language_code))

    def test_language_content_duplicate(self):
        """
        LanguageContent has the unique on the language_code field
        """
        with self.assertRaises(IntegrityError):
            LanguageContent(
                language_code='en',
                type='ui',
                content="{'test': 'test'}").save()

            LanguageContent(
                language_code='en',
                type='ui',
                content="{'test': 'test'}").save()
