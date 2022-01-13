from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import escape, format_html
from oauth2_provider.models import (AccessToken, Application, Grant,
                                    RefreshToken)

from .models import Category, Map, Node

# Register your models here.


class MapAdmin(admin.ModelAdmin):
    list_display = 'thumb', 'title', 'synopsis',
    search_fields = 'title', 'synopsis'

    def thumb(self, obj):
        if obj.project_cover:
            return format_html(f'<img src="{escape(obj.project_cover.url)}" width="100" />')
        return "Sem capa"


class NodeAdmin(admin.ModelAdmin):
    list_display = 'thumb', 'title', 'label', 'namespace', 'index', 'x_position', 'y_position',
    search_fields = 'title', 'label', 'namespace', 'text',

    def thumb(self, obj):
        if obj.button_icon:
            return format_html(f'<img src="{escape(obj.button_icon.url)}" width="100" />')
        return f"Sem ícone (#{obj.id})" if obj.id else "Sem ícone"

admin.site.register(Map, MapAdmin)
admin.site.register(Node, NodeAdmin)


admin.site.unregister(Group)
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)
