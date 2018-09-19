from django.contrib import admin
from json_field import JSONField
from jsoneditor.forms import JSONEditor

from content.models import EmailContent, LanguageContent


class EmailContentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'type', 'language_code')


class LanguageContentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }

    list_display = ('id', 'updated_at', 'language_code', 'type')


admin.site.register(EmailContent, EmailContentAdmin)
admin.site.register(LanguageContent, LanguageContentAdmin)

