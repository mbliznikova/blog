# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 02:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='article',
        ),
    ]
