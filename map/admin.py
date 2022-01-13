from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import escape, format_html
from oauth2_provider.models import (AccessToken, Application, Grant,
                                    RefreshToken)

from .models import Category, Map, Node, NodeMapping

# Register your models here.


# region Inlines
class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0


class NodeMappingInline(admin.TabularInline):
    model = NodeMapping
    extra = 0

# endregion


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'map', 'order', 'title', 'color', 'show', 'min_size', 'max_size', 'height_area'
    ordering = 'map', 'order',

    def color(self, obj):
        if obj.node_color:
            return format_html(f'<div title="{obj.node_color}" style="background-color: {obj.node_color};width:50px;height:50px;"></div>')
        return "Sem cor"
    color.short_description = 'Cor'

class MapAdmin(admin.ModelAdmin):
    list_display = 'thumb', 'title', 'synopsis',
    search_fields = 'title', 'synopsis'
    inlines = CategoryInline, NodeMappingInline,

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


class NodeMappingAdmin(admin.ModelAdmin):
    list_display = 'source', 'target', 'context', 'map'
    search_fields = 'source__title', 'target__title', 'context'
    list_filter = 'map',


admin.site.register(Category, CategoryAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeMapping, NodeMappingAdmin)


admin.site.unregister(Group)
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)
