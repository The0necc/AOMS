# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-09 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0005_auto_20191209_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpu',
            name='asset',
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_core_count',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='CPU核数'),
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
        migrations.DeleteModel(
            name='CPU',
        ),
    ]
