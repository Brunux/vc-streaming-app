# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-21 17:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamingapp', '0002_streaming_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streaming',
            old_name='name',
            new_name='title',
        ),
    ]
