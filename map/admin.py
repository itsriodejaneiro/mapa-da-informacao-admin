from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.fields import CharField
from django.utils.html import escape, format_html
from oauth2_provider.models import (AccessToken, Application, Grant,
                                    RefreshToken)
from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from .models import Category, Map, Node, NodeMapping

# Register your models here.


# region Inlines
class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0
    filter_horizontal = 'nodes',


class NodeMappingInline(admin.TabularInline):
    model = NodeMapping
    extra = 0

# endregion


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'title', 'map', 'order', 'color', 'show', 'min_size', 'max_size', 'height_area', 'node_count'
    ordering = 'map', 'order',
    list_filter = 'map',
    filter_horizontal = 'nodes',
    search_fields = 'title',

    def color(self, obj):
        if obj.node_color:
            return format_html(f'<div title="{obj.node_color}" style="background-color: {obj.node_color};width:50px;height:50px;border-radius:50px"></div>')
        return "Sem cor"
    color.short_description = 'Cor'

    def node_count(self, obj):
        return obj.nodes.count()
    node_count.short_description = 'Nós'


class MapAdmin(admin.ModelAdmin):
    list_display = 'title', 'cover', 'title_seo', '_image_seo', 'site_name_seo', 'categories_count', 'node_mapping_count',
    search_fields = 'title', 'synopsis'
    # inlines = CategoryInline, NodeMappingInline,

    def cover(self, obj):
        if obj.project_cover:
            return format_html(f'<img src="{escape(obj.project_cover.url)}" width="100" />')
        return "Sem capa"
    
    def _image_seo(self, obj):
        if obj.image_seo:
            return format_html(f'<img src="{escape(obj.image_seo.url)}" width="100" />')
        return "Sem imagem"

    def node_mapping_count(self, obj):
        return obj.node_mappings.count()
    node_mapping_count.short_description = 'Mapeamentos'

    def categories_count(self, obj):
        return obj.categories.count()
    categories_count.short_description = 'Categorias'


class NodeAdmin(admin.ModelAdmin):
    list_display = 'title', 'icone', 'button_icon', 'label', 'namespace', 'index', 'x_position', 'y_position', # 'slug',
    search_fields = 'title', 'label', 'namespace', 'text',
    list_filter = 'categories__map',
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(slug=Concat(F('namespace'), Value(' - '), F('label'), Value(' - '), F('index', output_field=CharField())))

    def icone(self, obj):
        if obj.button_icon:
            return format_html(f'<img src="{escape(obj.button_icon.url)}" width="100" />')
        return f"Sem ícone (#{obj.id})" if obj.id else "Sem ícone"

    def slug(self, obj):
        return obj.slug


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
