from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Category, Map, Node, NodeMapping


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class NodeMappingSerializer(serializers.ModelSerializer):
    source = NodeSerializer()
    target = NodeSerializer()
    context = serializers.SerializerMethodField()

    class Meta:
        model = NodeMapping
        fields = '__all__'

    def get_context(self, obj):
        if obj.context:
            return [s.strip() for s in obj.context.split(',')]
        return obj.context


class MapSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    node_mappings = NodeMappingSerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = '__all__'


class MapViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MapSerializer
    permission_classes = AllowAny,
    queryset = Map.objects.all().order_by('title').prefetch_related('node_mappings', 'node_mappings__source',
                                                                    'node_mappings__target', 'categories', 'categories__nodes')

    # todo: apply in get as well
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(queryset, many=True).data

        for map in data:
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
                    nodes_by_context[context] = nodes_by_context.get(context, []) + [source]
                    nodes_by_context[context] = nodes_by_context.get(context, []) + [target]

                nodes_contexts[source] = [*nodes_contexts.get(source, []), context]
                nodes_contexts[target] = [*nodes_contexts.get(target, []), context]

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

        return Response(data)
