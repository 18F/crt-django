# Generated by Django 2.2.4 on 2019-12-04 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cts_forms', '0024_insert_hate_trafficking_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='hatecrimes_trafficking',
            field=models.ManyToManyField(blank=True, null=True, to='cts_forms.HateCrimesandTrafficking'),
        ),
    ]