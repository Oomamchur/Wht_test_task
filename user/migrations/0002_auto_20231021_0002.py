from django.db import migrations
from django.db.migrations import RunPython


def func(apps, schema_editor) -> None:
    from django.core.management import call_command

    call_command("loaddata", "fixture_data.json")


def reverse_func(apps, schema_editor) -> None:
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [RunPython(func, reverse_func)]
