from django.db import models
from jsoneditor.fields.django_json_field import JSONField

from content.helper import OverwriteStorage


class EmailContent(models.Model):
    """
    This is the content of the email with specific type. The user can input
    the content with plain text and HTML.

    Type and language code is unique together, so only one content for
    specific type each language code
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    html = models.TextField()

    def __str__(self):
        return self.subject


class JSONContent(models.Model):
    """
    The idea of JSON Content:
    We have many different the content on the frontend, like the following:
    - Content by language for each page
    - Specific data on specific page
    - Specific data which not possible to put it on database
    - Specific data should be on the JSON type
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    content = JSONField()

    def __str__(self):
        return self.title


class MediaContent(models.Model):
    """
    The media content is feature to save an image file.
    And the field is a content type as page to manage the image is related
    to the one page.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to='media-content', storage=OverwriteStorage())

    def __str__(self):
        return self.title
