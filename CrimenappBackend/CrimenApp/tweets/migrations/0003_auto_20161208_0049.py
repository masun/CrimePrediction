# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-08 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_auto_20161208_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='como',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='cuando',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='donde',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='fecha',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='que',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tweets',
            name='texto',
            field=models.CharField(max_length=140, null=True, unique=True),
        ),
    ]
