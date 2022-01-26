from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.db.models import CharField, Count, Q, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment
from oauth2_provider.models import (AccessToken, Application, Grant, IDToken,
                                    RefreshToken)

from .models import Category, Map, Node, NodeMapping

# Register your models here.

# region Forms


class MapModelForm(forms.ModelForm):
    summary = forms.CharField(widget=forms.Textarea, label="Resumo",
                              help_text="Resumo do mapa (página de projetos) <br> Máx: 300 caracteres")

    class Meta:
        model = Map
        fields = '__all__'
        labels = {
            'editors': _('Editores e colaboradores'),
        }
        help_texts = {
            'synopsis': _('Sinopse do mapa (página de mapa). <br> Máx: 500 caracteres.'),
            'url_map': _('URL do mapa <br> Ex.: www.mapadainformacao.com.br/projetos/url-do-mapa/<br> Máx: 100 caracteres'),
            'title_seo': _('Ex.: Governo e Gestão de Documentos do Cidadão<br> Máx: 255 caracteres'),
            'description_seo': _('Ex.: Como o governo armazena e processa as informações de identificação dos cidadãos?<br> Máx: 255 caracteres'),
            'site_name_seo': _('Ex.: Mapa da Informação do Sistema de Identificação Brasileiro<br> Máx: 255 caracteres'),
            'editors': _('Editores ou colaboradores que podem acessar este mapa.<br>'),
        }


class CategoryModelForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

        help_texts = {
            'title': _('Máx: 255 caracteres.'),
            'description': _('Máx: 300 caracteres'),
            'node_color': _('Cor do nó em hexadecimal. <br>Ex.: #FFFFFF'),
            'min_size': _('Tamanho mínimo do nó em pixels. <br>Ex.: 10.0'),
            'max_size': _('Tamanho máximo do nó em pixels. <br>Ex.: 22.2'),
            'height_area': _('Altura da área da camada em pixels. <br>Ex.: 200.1'),
            # 'show': _('Exibir ou não a camada na página de mapa.'),

        }


class NodeModelForm(forms.ModelForm):

    class Meta:
        model = Node
        fields = '__all__'

        help_texts = {
            'title': _('Máx: 255 caracteres.'),
            'label': _('Máx: 255 caracteres.'),
            'text': _('Editor WYSIWYG<br>Máx: 300 caracteres.'),
            'x_position': _('Posição horizontal do nó em pixels <br>Ex.: 30.5.'),
            'y_position': _('Posição vertical do nó em pixels <br>Ex.: 30.5.'),
            'namespace': _('Facilitador<br> Ex: Nome do mapa - Camada <br>Máx: 255 caracteres.'),
            'index': _('Facilitador<br> Para nós com mesmo nome <br> Ex: 3'),
            'button_text': _('Máx: 255 caracteres.'),
            'button_link': _('Sempre incluir url completa.<br> Ex.: https://www.google.com<br>Máx: 255 caracteres.'),
        }


class NodeMappingModelForm(forms.ModelForm):

    class Meta:
        model = NodeMapping
        fields = '__all__'

        help_texts = {
            'context': _('Ex: adm2,sis3,fav5<br>Máx: 255 caracteres.'),
        }


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
                Q(source__id__in=node_id) | Q(target__id__in=node_id),
            )
        return queryset


class MapCustomFilter(admin.SimpleListFilter):
    title = _('Map')
    parameter_name = 'map'

    def lookups(self, request, model_admin):
        queryset = Map.objects.all()
        if not request.user.is_superuser:
            queryset = queryset.filter(editors=request.user)
        return queryset.values_list('id', 'title')

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(map=value)
        return queryset


class NodeMapFilter(admin.SimpleListFilter):
    title = _('Map')
    parameter_name = 'map'

    def lookups(self, request, model_admin):
        queryset = Map.objects.all()
        if not request.user.is_superuser:
            queryset = queryset.filter(editors=request.user)
        return queryset.values_list('id', 'title')

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(categories__map=value)
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


class MyUserAdmin(UserAdmin):
    list_display = 'id', 'username', 'name', 'email', 'is_superuser', 'my_groups',

    fieldsets = (
        ("Informações de login", {
            'fields': ('username', 'password',)
        }),
        ("Informações Pessoais", {
            'fields': ('email', 'first_name', 'last_name',)
        }),
        ("Permissões", {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')
        }),
        (None, {
            'fields': ('last_login', 'date_joined')
        }),
    )
    readonly_fields = ('last_login', 'date_joined',)

    def my_groups(self, obj):
        groups = obj.groups.all()
        if groups.count():
            groups = '<br>'.join(list(obj.groups.all().values_list('name', flat=True)))
            return format_html(f'{groups}')
        return "-"
    my_groups.short_description = 'grupos'

    def name(self, obj):
        return obj.get_full_name()
    name.short_description = 'Nome'

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser and not obj.id:
            obj.is_staff = True
            obj.is_active = True
            obj.save()


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'map', 'order', 'color', 'show', 'min_size', 'max_size', 'height_area', 'node_count'
    ordering = 'map', 'order',
    search_fields = 'title',
    exclude = 'show',
    list_filter = MapCustomFilter,
    filter_horizontal = 'nodes',
    form = CategoryModelForm

    def get_queryset(self, request):
        # If is superuser, show all, else only the ones they're editors
        queryset = super().get_queryset(request)\
            .select_related('map')\
            .annotate(node_count=Count('nodes'))

        if not request.user.is_superuser:
            queryset = queryset.filter(map__editors=request.user)
        return queryset

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['map'].queryset = Map.objects.filter(editors=request.user)
        return super(CategoryAdmin, self).render_change_form(request, context, *args, **kwargs)

    def color(self, obj):
        if obj.node_color:
            return format_html(f'<div title="{obj.node_color}" style="background-color: {obj.node_color};width:50px;height:50px;border-radius:50px"></div>')
        return "Sem cor"
    color.short_description = 'Cor'

    def node_count(self, obj):
        return obj.node_count
    node_count.short_description = 'Nós'


class MapAdmin(SummernoteModelAdmin):
    list_display = 'title', 'categories_link', 'node_mapping_link', 'cover', 'title_seo', '_image_seo', 'site_name_seo',
    search_fields = 'title', 'synopsis'
    form = MapModelForm
    filter_horizontal = 'editors',
    exclude = 'draft_password',
    summernote_fields = 'synopsis',

    def get_queryset(self, request):
        # If is superuser, show all maps, else, only the ones they're editors
        if request.user and request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(editors=request.user)

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
    categories_link.short_description = 'Camadas'

    def node_mapping_link(self, obj):
        count = obj.node_mappings.count()
        url = reverse('admin:map_nodemapping_changelist',) + f'?map__id__exact={obj.id}'
        return format_html(u'<a href="{}" target="_blank"> Ver {} </a>', url, count)
    node_mapping_link.short_description = 'Mapeamentos'

    # enable 'editors' field only for superusers
    def get_fields(self, request, obj=None):
        fields = super(MapAdmin, self).get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != 'editors']
        return fields


class NodeAdmin(SummernoteModelAdmin):
    list_display = 'id', 'title', 'icone', 'namespace', 'label', 'index', 'x_position', 'y_position',  # 'slug',
    search_fields = 'title', 'label', 'namespace', 'text',
    ordering = 'title',
    exclude = '_id',
    list_filter = NodeMapFilter,
    summernote_fields = 'text',
    form = NodeModelForm

    def get_queryset(self, request):
        # If is superuser, show all, else only the ones they're editors
        if request.user and request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(categories__map__editors=request.user)

    def icone(self, obj):
        if obj.button_icon:
            return format_html(f'<img src="{escape(obj.button_icon.url)}" width="30" />')
        return f"Sem ícone (#{obj.id})" if obj.id else "Sem ícone"

    def slug(self, obj):
        return obj.slug


class NodeMappingAdmin(admin.ModelAdmin):
    list_display = 'id', 'source', 'target', 'context', 'map'
    search_fields = 'source__title', 'target__title', 'source__label', 'target__label', 'context'
    list_filter = MapCustomFilter, NodeMappingNodeFilter,
    autocomplete_fields = 'source', 'target',
    form = NodeMappingModelForm

    def get_queryset(self, request):
        # If is superuser, show all, else only the ones they're editors
        if request.user and request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(map__editors=request.user)

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['map'].queryset = Map.objects.filter(editors=request.user)
        return super(NodeMappingAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeMapping, NodeMappingAdmin)

# replace default user admin with custom
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.unregister(Group)
admin.site.unregister(Attachment)
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)

try:
    admin.site.unregister(IDToken)
except:
    pass
