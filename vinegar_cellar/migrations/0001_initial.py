# Generated by Django 3.1 on 2020-08-05 19:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import vinegar_cellar.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barrel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wood_type', models.CharField(max_length=50)),
                ('capability', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BarrelSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1984), vinegar_cellar.models.max_value_current_year], verbose_name='year')),
            ],
        ),
        migrations.CreateModel(
            name='OperationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('schema', jsonfield.fields.JSONField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('values', jsonfield.fields.JSONField(default=[])),
                ('barrel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinegar_cellar.barrel')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinegar_cellar.operationtype')),
            ],
        ),
        migrations.AddField(
            model_name='barrel',
            name='barrel_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinegar_cellar.barrelset'),
        ),
    ]
