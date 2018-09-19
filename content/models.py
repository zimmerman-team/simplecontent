from django.db import models
from jsoneditor.fields.django_json_field import JSONField

LANGUAGES = (
    ('en', 'English'),
)


class EmailContent(models.Model):
    """
    This is the content of the email with specific type. The user can input
    the content with plain text and HTML.

    Type and language code is unique together, so only one content for
    specific type each language code
    """

    SHARE_LINK = 'share_link'
    EMAIL_TYPES = (
        (SHARE_LINK, 'Share Link'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=15, choices=EMAIL_TYPES)
    language_code = models.CharField(max_length=2, choices=LANGUAGES)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    html = models.TextField()

    class Meta:
        unique_together = ('type', 'language_code')

    def __str__(self):
        return self.subject


class LanguageContent(models.Model):
    """
    The model for upload the content of the portal in the JSON file.

    The user admin can change the content on the local machine and then
    upload to this model, after the file uploaded is succeeded
    the content of the portal will be changed automatically
    as with the uploaded json file.
    """
    UI = 'ui'
    FUNDING_GOES = 'funding_goes'
    CONTENT_TYPES = (
        (UI, 'UI'),
        (FUNDING_GOES, 'Funding Goes')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=15, choices=CONTENT_TYPES)
    language_code = models.CharField(max_length=2, choices=LANGUAGES)
    content = JSONField()

    class Meta:
        unique_together = ('type', 'language_code')

    def __str__(self):
        return '{type}, {language_code}'.format(
            type=self.type, language_code=self.language_code)
