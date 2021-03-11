# Generated by Django 2.2.17 on 2021-03-11 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cts_forms', '0101_auto_20210310_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaiverEmailReportCount',
            fields=[
                ('report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='waiver_email_report_count', serialize=False, to='cts_forms.AmericaReport')),
                ('email_count', models.IntegerField()),
            ],
            options={
                'db_table': 'waiver_email_report_count',
                'managed': False,
            },
        ),
    ]
