# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-10 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0014_auto_20191210_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='capacity',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='磁盘容量(GB)'),
        ),
    ]
