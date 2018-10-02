from django.contrib import admin
from json_field import JSONField
from jsoneditor.forms import JSONEditor

from content.models import EmailContent, LanguageContent, MediaContent


class EmailContentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'updated_at', 'language_code', 'content_type', 'subject')


class LanguageContentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    list_display = ('id', 'updated_at', 'language_code', 'content_type')


class MediaContentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'updated_at', 'title', 'slug', 'content_type', 'image')
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(EmailContent, EmailContentAdmin)
admin.site.register(LanguageContent, LanguageContentAdmin)
admin.site.register(MediaContent, MediaContentAdmin)
