from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import escape, format_html
from oauth2_provider.models import (AccessToken, Application, Grant,
                                    RefreshToken)

from .models import Map

# Register your models here.


class MapAdmin(admin.ModelAdmin):
    list_display = 'thumb', 'title', 'synopsis',
    search_fields = 'title', 'synopsis'

    def thumb(self, obj):
        if obj.project_cover:
            return format_html(f'<img src="{escape(obj.project_cover.url)}" width="100" />')
        return "Sem capa"


admin.site.register(Map, MapAdmin)


admin.site.unregister(Group)
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)
