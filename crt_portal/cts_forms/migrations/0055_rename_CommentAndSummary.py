# Generated by Django 2.2.11 on 2020-03-12 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cts_forms', '0054_report_public_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InternalHistory',
            new_name='CommentAndSummary',
        ),
    ]
