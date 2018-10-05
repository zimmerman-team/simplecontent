from django.contrib import admin

from content.models import (
    EmailContent, MediaContent, JSONContent
)


class EmailContentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'updated_at', 'title', 'slug', 'subject')


class MediaContentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'updated_at', 'title', 'slug', 'image')
    prepopulated_fields = {"slug": ("title", )}


class JSONContentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'updated_at', 'title', 'slug')
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(EmailContent, EmailContentAdmin)
admin.site.register(MediaContent, MediaContentAdmin)
admin.site.register(JSONContent, JSONContentAdmin)
