# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-09 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0003_auto_20191209_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='c_status',
        ),
        migrations.AddField(
            model_name='asset',
            name='c_status',
            field=models.BooleanField(default=True, verbose_name='今日是否采集'),
        ),
    ]
