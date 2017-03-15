# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 11:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0006_feedback_manual_grading'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='human_grader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]