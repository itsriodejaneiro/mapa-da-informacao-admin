from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import CharField, F, Q, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment
from oauth2_provider.models import (AccessToken, Application, Grant,
                                    RefreshToken)

from .models import Category, Map, Node, NodeMapping

# Register your models here.

# region Forms


class MapModelForm(forms.ModelForm):
    summary = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Map
        fields = '__all__'


# endregion

# region Filters

class NodeMappingNodeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Node')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'has_node'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return Node.objects.all()\
            .annotate(slug=Concat('namespace', Value(' - '), 'label', output_field=CharField()))\
            .order_by('slug')\
            .values_list('id', 'slug')

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        node_id = self.value()

        if node_id:
            node_id = node_id.split(',')
            return queryset.filter(
                Q(source__id__in=node_id)|Q(target__id__in=node_id),
            )
        return queryset

# endregion

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
    list_display = 'title', 'categories_link', 'node_mapping_link', 'cover', 'title_seo', '_image_seo', 'site_name_seo',
    search_fields = 'title', 'synopsis'
    form = MapModelForm
    exclude = 'draft_password',
    # inlines = CategoryInline, NodeMappingInline,

    def cover(self, obj):
        if obj.project_cover:
            return format_html(f'<img src="{escape(obj.project_cover.url)}" width="100" />')
        return "Sem capa"

    def _image_seo(self, obj):
        if obj.image_seo:
            return format_html(f'<img src="{escape(obj.image_seo.url)}" width="100" />')
        return "Sem imagem"

    def categories_link(self, obj):
        count = obj.categories.count()
        url = reverse('admin:map_category_changelist',) + f'?map__id__exact={obj.id}'
        return format_html(u'<a href="{}" target="_blank"> Ver {} </a>', url, count)
    categories_link.short_description = 'Categorias'

    def node_mapping_link(self, obj):
        count = obj.node_mappings.count()
        url = reverse('admin:map_nodemapping_changelist',) + f'?map__id__exact={obj.id}'
        return format_html(u'<a href="{}" target="_blank"> Ver {} </a>', url, count)
    node_mapping_link.short_description = 'Mapeamentos'


class NodeAdmin(SummernoteModelAdmin):
    list_display = 'id', 'title', 'icone', 'namespace', 'label', 'index', 'x_position', 'y_position',  # 'slug',
    search_fields = 'title', 'label', 'namespace', 'text',
    list_filter = 'categories__map',
    ordering = 'title',
    summernote_fields = 'text',

    def icone(self, obj):
        if obj.button_icon:
            return format_html(f'<img src="{escape(obj.button_icon.url)}" width="30" />')
        return f"Sem ícone (#{obj.id})" if obj.id else "Sem ícone"

    def slug(self, obj):
        return obj.slug


class NodeMappingAdmin(admin.ModelAdmin):
    list_display = 'id', 'source', 'target', 'context', 'map'
    search_fields = 'source__title', 'target__title', 'source__label', 'target__label', 'context'
    list_filter = 'map', NodeMappingNodeFilter,
    autocomplete_fields = 'source', 'target',


admin.site.register(Category, CategoryAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeMapping, NodeMappingAdmin)


admin.site.unregister(Group)
admin.site.unregister(Attachment)
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)
