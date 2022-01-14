from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

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
    queryset = Map.objects.all().order_by('title').prefetch_related('node_mappings', 'node_mappings__source', 'node_mappings__target', 'categories', 'categories__nodes')
