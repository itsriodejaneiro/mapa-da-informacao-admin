import json

import requests
from django.core.management import BaseCommand
from map.models import Category, Map, Node, NodeMapping

# Read old map API
source_url = "https://prod-mapa-da-informacao-admin.herokuapp.com/maps"
response = requests.get(source_url)
maps = response.json()

# Save map object to file
with open('maps.json', 'w') as f:
    json.dump(maps, f)


# TODO: REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Map.objects.all().delete()
# TODO: REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Category.objects.all().delete()
# TODO: REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Node.objects.all().delete()


# Objects keys
map_image_fields = 'project_cover', 'image_seo'
map_keys = 'title', 'synopsis', 'draft_password', 'url_map', 'title_seo', 'description_seo', 'site_name_seo',

category_keys = 'title', 'description', 'node_color', 'order', 'min_size', 'max_size', 'height_area', 'show',

node_image_fields = 'button_icon',
node_keys = 'title', 'label', 'text', 'x_position', 'y_position', 'namespace', 'index', 'button_text', 'button_link', '_id'


def get_image(image_field):
    """ extract image from strapi API's image field into local file """
    url = image_field['url']
    filename = image_field['name']
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
        return filename


def save_node_button_img(node, img):
    # img = node.get('button_icon')
    if img:
        # save locally
        image_location_on_drive = get_image(img)
        # upload to ImageField
        with open(image_location_on_drive, 'rb') as image:
            node.button_icon.save(image_location_on_drive, image)


def get_node_ids():
    return set(Node.objects.all().values_list('_id', flat=True))


existing_node_ids = get_node_ids()

for map in maps:

    # copy map data
    print('Importing map {}'.format(map["title"]))
    map_data = {}
    for key, value in map.items():
        if key in map_keys:
            map_data[key] = value
    new_map = Map.objects.create(**map_data)

    # save images
    for field_name in map_image_fields:
        if map.get(field_name):
            # save locally
            image_location_on_drive = get_image(map[field_name])
            # upload to ImageField
            field = getattr(new_map, field_name)
            with open(image_location_on_drive, 'rb') as image:
                field.save(image_location_on_drive, image)

    # __________________________________________________________________________________________________

    for category in map['categories']:
        print('\t Categoria: {}'.format(category["title"]))
        category_data = {key: category.get(key) for key in category_keys}
        category_instance = Category.objects.create(**category_data, map=new_map)

        node_instances = []  # queue for bulk create
        existing_nodes = []  # will be saved to this category
        for node in category['nodes']:

            # If exists, skip creation
            _id = node['_id']
            if _id in existing_node_ids:
                # print(f'\t\t nó {_id} já existente')
                node_instance = Node.objects.filter(_id=_id).first()
                existing_nodes.append(node_instance)
                existing_node_ids.add(_id)

            else:
                # Assemble node
                node_data = {key: node.get(key) for key in node_keys}
                node_instance = Node.objects.create(**node_data)
                node_instances.append(node_instance)
                print('\t\t\t',node['slug'])
                save_node_button_img(node_instance, node.get('button_icon'))

        # Create node instances and add to category
        # Node.objects.bulk_create(node_instances)

        # node_instances_ids = [node.id for node in node_instances]
        category_instance.nodes.add(*node_instances)
        category_instance.nodes.add(*existing_nodes)

    # __________________________________________________________________________________________________

    existing_node_ids = get_node_ids()
    print('\t NodeMappings')
    for node_mapping in map['node_mapping']:
        print('\t\t {} => {}'.format(node_mapping['source']['slug'], node_mapping['target']['slug']))
        node_mapping_data = {}
        if node_mapping.get('context'):
            node_mapping_data['context'] = node_mapping.get('context')

        # Find or create source
        source_data = node_mapping.get('source')
        if source_data['id'] in existing_node_ids:
            source = Node.objects.filter(_id=source_data['id']).first()
            # print(f'\t\t source {_id} já existente')
        else:
            data = {key: source_data.get(key) for key in node_keys}
            source = Node.objects.create(**data)
            save_node_button_img(source, source_data.get('button_icon'))

        # Find or create target
        target_data = node_mapping.get('target')
        if target_data['id'] in existing_node_ids:
            target = Node.objects.filter(_id=target_data['id']).first()
            # print(f'\t\t target {_id} já existente')
        else:
            data = {key: target_data.get(key) for key in node_keys}
            target = Node.objects.create(**data)
            save_node_button_img(target, target_data.get('button_icon'))

        node_mapping_data['source'] = source
        node_mapping_data['target'] = target

        # Parse context from list to comma separated string
        context = node_mapping_data.get('context')
        if context:
            node_mapping_data['context'] = ','.join([s.strip() for s in context])
        NodeMapping.objects.create(**node_mapping_data, map=new_map)


class Command(BaseCommand):
    help = 'Import old maps'

    def handle(self, *args, **options):
        pass
