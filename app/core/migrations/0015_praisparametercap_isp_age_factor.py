# Generated by Django 3.1.3 on 2020-12-10 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20201210_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='praisparametercap',
            name='isp_age_factor',
            field=models.DecimalField(decimal_places=2, default=2.5, max_digits=4),
            preserve_default=False,
        ),
    ]
