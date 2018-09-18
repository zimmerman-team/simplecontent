from rest_framework import serializers


class ShareLinkSerializer(serializers.Serializer):
    language_code = serializers.CharField()
    email = serializers.CharField()
    link = serializers.CharField()
