# Generated by Django 4.0.1 on 2022-01-24 18:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('map', '0008_map_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='editors',
            field=models.ManyToManyField(related_name='maps', to=settings.AUTH_USER_MODEL, verbose_name='Editores'),
        ),
    ]
