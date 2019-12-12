# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-10 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0015_auto_20191210_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ram',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='sn',
        ),
        migrations.AlterField(
            model_name='ram',
            name='capacity',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='内存大小'),
        ),
    ]