from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import BaseModelAdmin

from custom_url.models import URL

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('title', 'shorten_url', 'origin_url', 'updated_at','owner')
    search_fields = ('title', 'owner', )
    readonly_fields = ('updated_at',)
    ordering = ('owner',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'origin_url',),
        }),
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

