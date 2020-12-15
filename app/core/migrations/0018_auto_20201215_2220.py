# Generated by Django 3.1.3 on 2020-12-15 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20201215_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='user',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
