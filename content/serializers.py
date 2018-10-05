from rest_framework import serializers

from content.models import MediaContent, JSONContent


class ShareLinkSerializer(serializers.Serializer):
    language_code = serializers.CharField()
    email = serializers.CharField()
    link = serializers.CharField()


class MediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ('id', 'title', 'slug', 'image')


class JSONContentSerializer(serializers.ModelSerializer):
    content = serializers.JSONField()

    class Meta:
        model = JSONContent
        fields = ('id', 'title', 'slug', 'content')
