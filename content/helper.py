import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework import permissions


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name,  max_length=None):
        """
        If file is already exists,
        remove it to make it always the same filename
        """
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))

        return name


class RemoteHostPermission(permissions.BasePermission):
    """
    Custom Permission is only for the host which is already registered
    on the settings.py of MAILGUN configuration.
    """

    def has_permission(self, request, view):
        if request.META.get('REMOTE_HOST') in \
                settings.SIMPLE_MAIL.get('REMOTE_HOST_PERMISSION') or \
                request.method == 'GET' or request.user.is_authenticated:
            return True

        return False
