import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from api import helper
from content.models import EmailContent


class ShareLink(views.APIView):
    """
    Simple send email for the share link
    """

    permission_classes = (helper.RemoteHostPermission, )

    def post(self, request, format=None):
        message = MIMEMultipart('alternative')

        message['From'] = settings.SIMPLE_MAIL.get('FROM_EMAIL')

        try:
            message['To'] = request.data.get('email')
            language_code = request.data.get('language_code')

            # Get content email for specific type and language
            email_content = EmailContent.objects.get(
                type=EmailContent.SHARE_LINK, language_code=language_code)

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

            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'message': 'Not acceptable!'})

        return Response(status=status.HTTP_200_OK,
                        data={'message': 'Success!'})
