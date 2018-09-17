from django.contrib import admin

from content.models import EmailContent, LanguageContent


class EmailContentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'type', 'language_code')


class LanguageContentAdmin(admin.ModelAdmin):
    list_display = ('language_code', 'json_file')


admin.site.register(EmailContent, EmailContentAdmin)
admin.site.register(LanguageContent, LanguageContentAdmin)

