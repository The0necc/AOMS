# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-09 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0007_auto_20191209_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('cpu_count', models.PositiveSmallIntegerField(default=1, verbose_name='物理CPU个数')),
                ('cpu_core_count', models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web_cmdb.Asset')),
            ],
            options={
                'verbose_name': 'CPU',
            },
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_count',
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_model',
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_physical_count',
        ),
    ]
