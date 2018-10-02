import factory

from factory import LazyAttribute
from factory.fuzzy import FuzzyText

from django.template.defaultfilters import slugify
from content.models import MediaContent


class MediaContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MediaContent

    title = FuzzyText()
    # For now is only 'home' content type on this model
    content_type = 'home'
    # create lazy slug
    slug = LazyAttribute(
        lambda media_content: slugify(media_content.title).lower())
    image = factory.django.ImageField(color='blue')
