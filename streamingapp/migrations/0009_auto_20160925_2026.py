# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-26 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamingapp', '0008_streaming_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streaming',
            name='image',
            field=models.ImageField(default=b'default.png', upload_to=b'streaming_images'),
        ),
    ]
