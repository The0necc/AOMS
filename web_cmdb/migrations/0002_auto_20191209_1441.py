# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-09 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP'),
        ),
        migrations.AddField(
            model_name='server',
            name='c_status',
            field=models.BooleanField(default=True, verbose_name='今日是否采集'),
        ),
    ]
