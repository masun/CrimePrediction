# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-08 00:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='como',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='cuando',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='donde',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='fecha',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='que',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='texto',
            field=models.CharField(default='', max_length=140),
        ),
    ]
