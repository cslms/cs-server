from __future__ import unicode_literals

from django.db import migrations


def make_languages(apps, schema_editor):
    # File formats
    from codeschool.core.files.models import format_processor

    def process(L):
        FileFormat = apps.get_model('files', 'fileformat')

        for kwargs in L:
            FileFormat.objects.get_or_create(**kwargs)

    format_processor(process)


class Migration(migrations.Migration):
    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_languages),
    ]
