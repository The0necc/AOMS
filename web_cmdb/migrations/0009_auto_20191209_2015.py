# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-09 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0008_auto_20191209_2007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpu',
            name='asset',
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_count',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='物理CPU个数'),
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_model',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号'),
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_physical_count',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='CPU核数'),
        ),
        migrations.DeleteModel(
            name='CPU',
        ),
    ]
