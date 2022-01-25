from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from html2text import re


class Command(BaseCommand):

    def handle(self, *args, **options):

        editor_group_name = 'editor(a)'
        editor_group = Group.objects.filter(name=editor_group_name).first()
        if editor_group:
            editor_permissions = editor_group.permissions.exclude(codename__icontains='add', content_type__model='map')
            editor_group.permissions.set(editor_permissions)

            return 'OK'
        return 'Group not found'
