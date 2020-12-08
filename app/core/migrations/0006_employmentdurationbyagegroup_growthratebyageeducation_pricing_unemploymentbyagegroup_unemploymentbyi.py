# Generated by Django 3.1.3 on 2020-11-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201029_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentDurationByAgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField()),
                ('age_group', models.CharField(max_length=255)),
                ('age_min', models.IntegerField()),
                ('age_max', models.IntegerField()),
                ('duration', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='GrowthRateByAgeEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('dropout', models.DecimalField(decimal_places=2, max_digits=5)),
                ('diploma', models.DecimalField(decimal_places=2, max_digits=5)),
                ('some_college', models.DecimalField(decimal_places=2, max_digits=5)),
                ('license', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bachelors', models.DecimalField(decimal_places=2, max_digits=5)),
                ('masters', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mba', models.DecimalField(decimal_places=2, max_digits=5)),
                ('attorney', models.DecimalField(decimal_places=2, max_digits=5)),
                ('doctorate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('professional', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField()),
                ('term', models.IntegerField()),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('min_cagr', models.DecimalField(decimal_places=2, max_digits=5)),
                ('targeted_cagr', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_cagr', models.DecimalField(decimal_places=2, max_digits=5)),
                ('payment_cap_factor', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prepayment_fv', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prepayment_growth', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='UnemploymentByAgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField()),
                ('age_group', models.CharField(max_length=255)),
                ('age_min', models.IntegerField()),
                ('age_max', models.IntegerField()),
                ('mean_duration', models.DecimalField(decimal_places=1, max_digits=4)),
                ('max_duration', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='UnemploymentByIndustry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField()),
                ('industry', models.CharField(max_length=255)),
                ('mean_duration', models.DecimalField(decimal_places=1, max_digits=4)),
                ('max_duration', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='UnemploymentByOccupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField()),
                ('occupation', models.CharField(max_length=255)),
                ('occupation_type', models.CharField(max_length=255)),
                ('mean_duration', models.DecimalField(decimal_places=1, max_digits=4)),
                ('max_duration', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
    ]