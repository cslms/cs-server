# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding_io', '0003_auto_20161214_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingiofeedback',
            name='is_pre_test',
            field=models.BooleanField(default=False),
        ),
    ]