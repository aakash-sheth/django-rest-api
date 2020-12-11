# Generated by Django 3.1.3 on 2020-12-10 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_hikesbyeducation'),
    ]

    operations = [
        migrations.CreateModel(
            name='PraisParameterCap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField(auto_now=True)),
                ('isa_processing_fee', models.DecimalField(decimal_places=3, max_digits=6)),
                ('isa_servicing_fee', models.DecimalField(decimal_places=3, max_digits=6)),
                ('isa_sales_charge', models.DecimalField(decimal_places=3, max_digits=6)),
                ('max_minimum_self_equity', models.DecimalField(decimal_places=3, max_digits=6)),
                ('annual_lower_income', models.DecimalField(decimal_places=2, max_digits=8)),
                ('isa_processing_fee_cap', models.DecimalField(decimal_places=2, max_digits=8)),
                ('buyout_servicing_fee', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
