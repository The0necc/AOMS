# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-09 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_cmdb', '0004_auto_20191209_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.SmallIntegerField(choices=[(0, '其它'), (1, '硬件变更'), (2, '新增配件'), (3, '设备下线'), (4, '设备上线'), (5, '定期维护'), (6, '业务上线\\更新\\变更')], default=4, verbose_name='事件类型')),
                ('component', models.CharField(blank=True, max_length=256, null=True, verbose_name='事件子项')),
                ('detail', models.TextField(verbose_name='事件详情')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='事件时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_cmdb.Asset')),
            ],
            options={
                'verbose_name': '事件纪录',
                'verbose_name_plural': '事件纪录',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产SN号')),
                ('asset_type', models.CharField(blank=True, choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('software', '软件资产')], default='server', max_length=64, null=True, verbose_name='资产类型')),
                ('manufacturer', models.CharField(blank=True, max_length=64, null=True, verbose_name='生产厂商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('ram_size', models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('cpu_count', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='CPU物理数量')),
                ('cpu_core_count', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='CPU核心数量')),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True, verbose_name='发行商')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='系统类型')),
                ('os_release', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统版本号')),
                ('data', models.TextField(verbose_name='资产数据')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='汇报日期')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='数据更新日期')),
                ('approved', models.BooleanField(default=False, verbose_name='是否批准')),
            ],
            options={
                'verbose_name': '新上线待批准资产',
                'verbose_name_plural': '新上线待批准资产',
                'ordering': ['-c_time'],
            },
        ),
        migrations.AddField(
            model_name='eventlog',
            name='new_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_cmdb.NewAssetApprovalZone'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_cmdb.User', verbose_name='事件执行人'),
        ),
    ]
