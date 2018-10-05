import factory

from factory import LazyAttribute
from factory.fuzzy import FuzzyText

from django.template.defaultfilters import slugify
from content.models import EmailContent, MediaContent, JSONContent


class EmailContentShareLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailContent

    title = 'Share Link'
    # create lazy slug
    slug = LazyAttribute(
        lambda media_content: slugify(media_content.title).lower())
    subject = 'Share Link'
    text = '{link}'
    html = '{link}'


class MediaContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MediaContent

    title = FuzzyText()
    # create lazy slug
    slug = LazyAttribute(
        lambda media_content: slugify(media_content.title).lower())
    image = factory.django.ImageField(color='blue')


class JSONContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JSONContent

    title = FuzzyText()
    # create lazy slug
    slug = LazyAttribute(
        lambda media_content: slugify(media_content.title).lower())
    content = '{"key": "value"}'
