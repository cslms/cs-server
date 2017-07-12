# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-27 14:42
from __future__ import unicode_literals

import codeschool.lms.activities.models.activity
import codeschool.mixins
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import wagtail.contrib.wagtailroutablepage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpartaActivity',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('author_name', models.CharField(blank=True, help_text="The author's name, if not the same user as the question owner.", max_length=100, verbose_name="Author's name")),
                ('visible', models.BooleanField(default=codeschool.lms.activities.models.activity.bool_to_true, help_text='Makes activity invisible to users.', verbose_name='Invisible')),
                ('closed', models.BooleanField(default=bool, help_text='A closed activity does not accept new submissions, but users can see that they still exist.', verbose_name='Closed to submissions')),
                ('group_submission', models.BooleanField(default=bool, help_text='If enabled, submissions are registered to groups instead of individual students.', verbose_name='Group submissions')),
                ('max_group_size', models.IntegerField(default=6, help_text='If group submission is enabled, define the maximum size of a group.', verbose_name='Maximum group size')),
                ('disabled', models.BooleanField(default=bool, help_text='Activities can be automatically disabled when Codeshool encounters an error. This usually produces a message saved on the .disabled_message attribute. This field is not controlled directly by users.', verbose_name='Disabled')),
                ('disabled_message', models.TextField(blank=True, help_text='Messsage explaining why the activity was disabled.', verbose_name='Disabled message')),
                ('has_submissions', models.BooleanField(default=bool)),
                ('has_correct_submissions', models.BooleanField(default=bool)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Sparta Activity',
                'verbose_name_plural': 'Sparta Activities',
            },
            bases=(codeschool.mixins.CommitMixin, wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='SpartaGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=140, verbose_name='Name')),
                ('status', models.IntegerField(choices=[(1, 'inactive'), (0, 'active')], default=1)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='sparta.SpartaActivity')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='SpartaMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('role', models.IntegerField(choices=[(0, 'tutor'), (1, 'learner')])),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='sparta.SpartaGroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sparta.SpartaActivity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='spartagroup',
            name='members',
            field=models.ManyToManyField(related_name='sparta_groups', through='sparta.SpartaMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usergrade',
            unique_together=set([('activity', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='spartamembership',
            unique_together=set([('user', 'group', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='spartagroup',
            unique_together=set([('name', 'activity')]),
        ),
    ]
