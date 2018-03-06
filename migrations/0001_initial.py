# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 12:08
from __future__ import unicode_literals

import Sanitizer.users.models
import Sanitizer.utilities.time_calculator.functions
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('birth_date', models.DateField(help_text=b"User's birth date", null=True)),
                ('mobile_number', models.CharField(blank=True, help_text='Mobile Number', max_length=40, null=True)),
                ('home_number', models.CharField(blank=True, help_text='Home Number', max_length=40, null=True)),
                ('contact_time_min', models.TimeField(blank=True, help_text='Contact user min time', null=True)),
                ('contact_time_max', models.TimeField(blank=True, help_text='Contact user max time', null=True)),
                ('address', models.CharField(blank=True, help_text='Address', max_length=60, null=True)),
                ('city', models.CharField(blank=True, help_text='City', max_length=60, null=True)),
                ('website', models.URLField(blank=True, help_text='Personal website', null=True)),
                ('avatar', models.ImageField(blank=True, default=b'', upload_to=Sanitizer.users.models.get_upload_path)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_activated', models.DateTimeField(blank=True, null=True)),
                ('hide_contact_details', models.NullBooleanField(default=None, help_text='Contact data will be hidden')),
                ('subscribed', models.BooleanField(default=True, help_text='Send emails')),
                ('activation_key', models.CharField(blank=True, max_length=40)),
                ('key_expires', models.DateTimeField(default=Sanitizer.utilities.time_calculator.functions.days_hence)),
                ('facebook_link', models.CharField(blank=True, help_text='Facebook profile link', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='simple_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
