# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-10 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0011_auto_20170309_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='final_feedback',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='submission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='activities.Submission'),
        ),
    ]