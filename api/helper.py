from django.conf import settings
from rest_framework import permissions


class RemoteHostPermission(permissions.BasePermission):
    """
    Custom Permission is only for the host which is already registered
    on the settings.py of MAILGUN configuration.
    """

    def has_permission(self, request, view):
        if request.META.get('REMOTE_HOST') in \
                settings.SIMPLE_MAIL.get('REMOTE_HOST_PERMISSION'):
            return True

        return False
