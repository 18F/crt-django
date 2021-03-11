# Generated by Django 2.2.17 on 2021-03-11 01:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cts_forms', '0099_covid_form_letter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protectedclass',
            name='protected_class',
            field=models.CharField(blank=True, choices=[('age', 'Age'), ('disability', 'Disability (including temporary or recovered and including HIV and drug addiction)'), ('family_status', 'Family, marital, or parental status'), ('gender', 'Gender identity (including gender stereotypes)'), ('genetic', 'Genetic information (including family medical history)'), ('immigration', 'Immigration/citizenship status (choosing this will not share your status)'), ('language', 'Language'), ('national_origin', 'National origin (including ancestry and ethnicity)'), ('pregnancy', 'Pregnancy'), ('race/color', 'Race/color'), ('religion', 'Religion'), ('sex', 'Sex'), ('orientation', 'Sexual orientation'), ('none', 'None of these apply to me'), ('other', 'Other reason')], max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='protectedclass',
            name='value',
            field=models.CharField(blank=True, choices=[('age', 'Age'), ('disability', 'Disability (including temporary or recovered and including HIV and drug addiction)'), ('family_status', 'Family, marital, or parental status'), ('gender', 'Gender identity (including gender stereotypes)'), ('genetic', 'Genetic information (including family medical history)'), ('immigration', 'Immigration/citizenship status (choosing this will not share your status)'), ('language', 'Language'), ('national_origin', 'National origin (including ancestry and ethnicity)'), ('pregnancy', 'Pregnancy'), ('race/color', 'Race/color'), ('religion', 'Religion'), ('sex', 'Sex'), ('orientation', 'Sexual orientation'), ('none', 'None of these apply to me'), ('other', 'Other reason')], max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='crt_reciept_year',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name=django.core.validators.MaxValueValidator(2021)),
        ),
        migrations.AlterField(
            model_name='report',
            name='intake_format',
            field=models.CharField(choices=[('web', 'Web'), ('letter', 'Letter'), ('phone', 'Phone'), ('fax', 'Fax'), ('email', 'Email')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='last_incident_year',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name=django.core.validators.MaxValueValidator(2021, message='Date can not be in the future.')),
        ),
        migrations.AlterField(
            model_name='report',
            name='primary_complaint',
            field=models.CharField(choices=[('voting', 'Voting rights or ability to vote affected'), ('workplace', 'Workplace discrimination or other employment-related problem'), ('housing', 'Housing discrimination or harassment'), ('education', 'Discrimination at a school, educational program or service, or related to receiving education'), ('police', 'Mistreated by police, correctional staff, or inmates'), ('commercial_or_public', 'Discriminated against in a commercial location or public place'), ('something_else', 'Something else happened')], default='', max_length=100),
        ),
        migrations.CreateModel(
            name='AmericaReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_first_name', models.CharField(blank=True, max_length=225, null=True)),
                ('contact_last_name', models.CharField(blank=True, max_length=225, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=225, null=True, validators=[django.core.validators.RegexValidator('^(?=^\\D*(\\d\\D*){7,15}$)(?=^(?:(?![a-zA-Z]).)*$).*$', message='If you submit a phone number, please make sure to include between 7 and 15 digits. The characters "+", ")", "(", "-", and "." are allowed. Please include country code if entering an international phone number.')])),
                ('contact_address_line_1', models.CharField(blank=True, max_length=225, null=True)),
                ('contact_address_line_2', models.CharField(blank=True, max_length=225, null=True)),
                ('contact_city', models.CharField(blank=True, max_length=700, null=True)),
                ('contact_state', models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('AS', 'American Samoa'), ('GU', 'Guam'), ('MP', 'Northern Mariana Islands'), ('PR', 'Puerto Rico'), ('VI', 'Virgin Islands'), ('AE', 'Armed Forces Africa'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Canada'), ('AE', 'Armed Forces Europe'), ('AE', 'Armed Forces Middle East'), ('AP', 'Armed Forces Pacific')], max_length=100, null=True)),
                ('contact_zip', models.CharField(blank=True, max_length=10, null=True)),
                ('agency', models.CharField(blank=True, max_length=225, null=True)),
                ('product_name', models.CharField(blank=True, max_length=225, null=True)),
                ('product_company', models.CharField(blank=True, max_length=225, null=True)),
                ('parent_company', models.CharField(blank=True, max_length=225, null=True)),
                ('unique_entity_identifer', models.CharField(blank=True, max_length=225, null=True)),
                ('duns_number', models.CharField(blank=True, max_length=225, null=True)),
                ('country_of_origin', models.CharField(blank=True, max_length=225, null=True)),
                ('purpose_of_product', models.CharField(max_length=7000)),
                ('market_justification', models.CharField(max_length=7000)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('status', models.TextField(choices=[('new', 'New'), ('open', 'Open'), ('denied', 'Denied'), ('approved', 'Approved')], default='new')),
                ('approver_final', models.CharField(blank=True, max_length=1000, null=True)),
                ('final_approval_date', models.DateTimeField()),
                ('closed_date', models.DateTimeField(blank=True, help_text='The Date this report\'s status was most recently set to "Closed"', null=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
