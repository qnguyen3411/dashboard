# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-12 00:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallApp', '0002_usermanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserManager',
        ),
    ]
