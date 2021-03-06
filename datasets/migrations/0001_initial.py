# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('data', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'Unprocessed'), (2, 'In Progress'), (3, 'Calculated'), (4, 'Error')], default=1)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ErrorsLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.CharField(max_length=15)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('msg', models.CharField(max_length=150)),
                ('traceback', models.TextField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.DataSet')),
            ],
        ),
    ]
