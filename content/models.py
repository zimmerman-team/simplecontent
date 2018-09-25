from django.db import models
from jsoneditor.fields.django_json_field import JSONField

from content.helper import OverwriteStorage

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
    content_type = models.CharField(max_length=15, choices=EMAIL_TYPES)
    language_code = models.CharField(max_length=2, choices=LANGUAGES)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    html = models.TextField()

    class Meta:
        unique_together = ('content_type', 'language_code')

    def __str__(self):
        return self.subject


class LanguageContent(models.Model):
    """
    The model of the JSON data.

    This feature to cover some static data in the frontend
    with ability to change it, like the following:
    - The UI static text, menu text, breadcrumb text, footer text.
    - Or just general JSON data is record type which needed
      to parse them on the frontend.
    """
    UI = 'ui'
    FUNDING_GOES = 'funding_goes'
    CONTENT_TYPES = (
        (UI, 'UI'),
        (FUNDING_GOES, 'Funding Goes')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=15, choices=CONTENT_TYPES)
    language_code = models.CharField(max_length=2, choices=LANGUAGES)
    content = JSONField()

    class Meta:
        unique_together = ('content_type', 'language_code')

    def __str__(self):
        return '{content_type}, {language_code}'.format(
            content_type=self.content_type, language_code=self.language_code)


class MediaContent(models.Model):
    """
    The media content is feature to save an image file.
    And the field is a content type as page to manage the image is related
    to the one page.
    """
    HOME = 'home'
    CONTENT_TYPES = (
        (HOME, 'Home'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=15, choices=CONTENT_TYPES)
    image = models.ImageField(
        upload_to='media-content', storage=OverwriteStorage())

    def __str__(self):
        return '{content_type}, {image_name}'.format(
            content_type=self.content_type, image_name=self.image.name)
