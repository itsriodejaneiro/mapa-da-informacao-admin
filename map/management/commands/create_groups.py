from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create groups with default permissions for editor and colaborator profiles'

    def handle(self, *args, **options):

        # Editor:
        # Ver e editar todos os mapas que ele criou ou tem permissão de ver
        editor_group_name = 'editor(a)'
        editor_group = Group.objects.filter(name=editor_group_name).first()
        if not editor_group:
            editor_group = Group.objects.create(name=editor_group_name)
        editor_permissions = Permission.objects.filter(
            content_type__app_label='map').exclude(codename__icontains='delete')
        # nao pode adicionar mapas
        editor_permissions = editor_permissions.exclude(codename__icontains='add', content_type__model='map')
        editor_group.permissions.set(editor_permissions)

        # Colaborador:
        # Ver todos os mapas que ele tem permissão de ver
        collaborator_group_name = 'colaborador(a)'
        collaborator_group = Group.objects.filter(name=collaborator_group_name).first()
        if not collaborator_group:
            collaborator_group = Group.objects.create(name=collaborator_group_name)

        collaborator_permissions = Permission.objects.filter(
            content_type__app_label='map', codename__icontains='view')
        collaborator_group.permissions.set(collaborator_permissions)

        return 'OK'