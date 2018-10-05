from rest_framework import serializers

from content.models import MediaContent


class ShareLinkSerializer(serializers.Serializer):
    language_code = serializers.CharField()
    email = serializers.CharField()
    link = serializers.CharField()


class MediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ('id', 'title', 'slug', 'image')
