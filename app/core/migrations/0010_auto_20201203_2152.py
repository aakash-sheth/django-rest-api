# Generated by Django 3.1.3 on 2020-12-03 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20201202_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unemploymentbyindustry',
            old_name='indutry_id',
            new_name='industry_id',
        ),
    ]