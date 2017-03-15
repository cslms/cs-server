from django.contrib.contenttypes.management import update_contenttypes
from django.db import migrations


def make_syspages(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'contenttype')
    update_contenttypes(apps.app_configs['contenttypes'])
    update_contenttypes(apps.app_configs['core'])

    # Hidden root
    content_type = ContentType.objects.get_or_create(model='hiddenroot',
                                                     app_label='core')[0]
    apps.get_model('core', 'hiddenroot').objects.create(
        path="00010002",
        depth=2,
        numchild=1,
        title="Hidden pages",
        slug="hidden",
        url_path="/hidden/",
        live=False,
        locked=True,
        content_type=content_type,
    )

    # Rogue root
    content_type = ContentType.objects.get_or_create(model='rogueroot',
                                                     app_label='core')[0]
    apps.get_model('core', 'rogueroot').objects.create(
        path="000100020001",
        depth=3,
        numchild=0,
        title="Pages with no parent",
        slug="rogue",
        url_path="/rogue/",
        live=False,
        locked=True,
        content_type=content_type,
    )

    # Fix the number of children in the root node
    page_cls = apps.get_model('wagtailcore', 'page')
    root = page_cls._default_manager.get(
        path='0001')  # .objects is not working (?!)
    root.numchild += 1
    root.save(update_fields=['numchild'])


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_initial_formats'),
        ('wagtailcore', '0002_initial_data'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(make_syspages),
    ]
