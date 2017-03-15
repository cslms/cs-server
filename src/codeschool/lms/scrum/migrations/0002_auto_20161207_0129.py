# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-07 03:29
from __future__ import unicode_literals

import codeschool.lms.scrum.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='duration_weeks',
            field=models.PositiveIntegerField(default=1, validators=[codeschool.lms.scrum.models.non_null]),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='scrum.ScrumProject'),
        ),
    ]