# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-10 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0010_auto_20191210_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='interface_type',
            field=models.CharField(default='unknown', max_length=32, verbose_name='接口类型'),
        ),
    ]