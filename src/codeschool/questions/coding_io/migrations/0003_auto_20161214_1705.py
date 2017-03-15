# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 17:05
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coding_io', '0002_codingiofeedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codingiofeedback',
            name='for_pre_tests',
        ),
        migrations.AddField(
            model_name='codingiofeedback',
            name='feedback',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]