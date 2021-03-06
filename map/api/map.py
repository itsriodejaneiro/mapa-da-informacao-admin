from http.client import ResponseNotReady
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.decorators import api_view
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Category, Map, Node, NodeMapping


def populate_context(map):
    nodes_relations = {}  # {node_id: [related_node_id]}
    nodes_by_context = {}  # key: context, value: list of nodes
    nodes_contexts = {}  # key: node id, value: list of contexts
    for node_mapping in map['node_mappings']:
        # Group by node_mapping
        source, target = node_mapping['source']['id'], node_mapping['target']['id']
        context_list = node_mapping.get('context')

        nodes_relations[source] = nodes_relations.get(source, []) + [target]
        nodes_relations[target] = nodes_relations.get(target, []) + [source]

        for context in context_list:
            nodes_by_context[context] = nodes_by_context.get(context, []) + [source, target]

        nodes_contexts[source] = [*nodes_contexts.get(source, []), *context_list]
        nodes_contexts[target] = [*nodes_contexts.get(target, []), *context_list]

    for category in map['categories']:
        # Apply relations to nodes
        for node in category['nodes']:
            node['related_nodes'] = nodes_relations.get(node['id'], [])

            node_contexts = set(nodes_contexts.get(node['id'], []))

            node['context'] = node_contexts
            for context_list in node_contexts:
                related_nodes_by_context = node.get('related_nodes_by_context', set())
                related_nodes_by_context.update(nodes_by_context.get(context_list, []))
                node['related_nodes_by_context'] = related_nodes_by_context

    return map


class NodeSerializer(ModelSerializer):

    class Meta:
        model = Node
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class NodeMappingSerializer(ModelSerializer):
    source = NodeSerializer()
    target = NodeSerializer()
    context = SerializerMethodField()

    class Meta:
        model = NodeMapping
        fields = '__all__'

    def get_context(self, obj):
        if obj.context:
            return [s.strip() for s in obj.context.split(',')]
        return obj.context


class MapSerializer(ModelSerializer):
    categories = SerializerMethodField()
    node_mappings = NodeMappingSerializer(many=True, read_only=True)

    def get_categories(self, obj):
        queryset = obj.categories.order_by('order')
        data = CategorySerializer(queryset, many=True, read_only=True).data
        return list(sorted(data, key=lambda x: x.get('order') or 0))
        
    class Meta:
        model = Map
        exclude = 'draft_password',


class MiniMapSerializer(ModelSerializer):

    class Meta:
        model = Map
        fields = 'id', 'title', 'synopsis', 'summary', 'project_cover', 'url_map',


class MapViewSet(ReadOnlyModelViewSet):
    serializer_class = MapSerializer
    permission_classes = AllowAny,
    queryset = Map.objects.filter(show=True).order_by('title').prefetch_related('node_mappings', 'node_mappings__source',
                                                                    'node_mappings__target', 'categories', 'categories__nodes')

    # todo: apply in get as well
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(queryset, many=True).data

        for map in data:
            map = populate_context(map)

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()
        data = serializer(instance).data

        data = populate_context(data)

        return Response(data)


@api_view(['GET'])
def mini_maps(request):
    # todo: cache
    # todo: clear cache on model
    queryset = Map.objects.filter(show=True).order_by('title')
    data = MiniMapSerializer(queryset, many=True).data
    return Response(data)
