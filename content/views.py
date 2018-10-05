import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, NotAcceptable, server_error

from content import helper, serializers
from content.models import (
    EmailContent, MediaContent, JSONContent
)

from content.serializers import MediaContentSerializer, JSONContentSerializer


class ShareLinkView(views.APIView):
    slug = 'share-link'

    @classmethod
    def get_serializer(cls):
        return serializers.ShareLinkSerializer()

    @classmethod
    def post(cls, request, *args, **kwargs):
        """
        The endpoint to sent an email share link.
        """
        message = MIMEMultipart('alternative')
        message['From'] = settings.SIMPLE_MAIL.get('FROM_EMAIL')

        try:
            message['To'] = request.data.get('email')

            # Get content email for specific type and language
            email_content = EmailContent.objects.get(slug=cls.slug)

            message['Subject'] = email_content.subject

            link = request.data.get('link')
            # Create the body of the message (a plain-text
            # and an HTML version).
            text = email_content.text.format(link=link)
            html = email_content.html.format(link=link)

            # Record the MIME types of both parts - text/plain and text/html.
            content_plain = MIMEText(text, 'plain')
            content_html = MIMEText(html, 'html')

            message.attach(content_plain)
            message.attach(content_html)

            smtp = smtplib.SMTP(settings.SIMPLE_MAIL.get('SMTP_HOSTNAME'), 587)

            smtp.login(settings.SIMPLE_MAIL.get('DEFAULT_SMTP_LOGIN'),
                       settings.SIMPLE_MAIL.get('DEFAULT_PASSWORD'))

            smtp.sendmail(
                message.get('From'), message.get('To'), message.as_string())
            smtp.quit()

        except Exception as e:
            logging.exception(e)

            # *** For security reason ***
            # If something errors when send an email,
            # just send to the client is not acceptable.
            # And for more detail about the error can check it
            # on the logging errors
            raise NotAcceptable

        return Response(
            status=status.HTTP_200_OK, data={'message': 'Success!'})


class MediaContentView(views.APIView):

    @classmethod
    def get(cls, request, *args, **kwargs):
        """
        The endpoint presents the media content by slug request.
        <br>
        **The media content** is endpoint to present the URL of the media file.
        """
        try:
            media_content = MediaContent.objects.get(slug=kwargs.get('slug'))
            serializer = MediaContentSerializer(media_content)

            return Response(serializer.data)
        except MediaContent.DoesNotExist:
            raise NotFound


class JSONContentView(views.APIView):

    @classmethod
    def get(cls, request, *args, **kwargs):
        """
        The endpoint presents the JSON content by slug request.
        <br>
        **The JSON content** is endpoint to present the JSON content.
        """
        try:
            json_content = JSONContent.objects.get(slug=kwargs.get('slug'))
            serializer = JSONContentSerializer(json_content)

            return Response(serializer.data)
        except MediaContent.DoesNotExist:
            raise NotFound
