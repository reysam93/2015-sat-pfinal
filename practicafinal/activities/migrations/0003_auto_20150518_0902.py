# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20150517_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpage',
            name='acts',
            field=models.ManyToManyField(to='activities.Activity'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpage',
            name='css',
            field=models.ForeignKey(to='activities.UserCSS'),
            preserve_default=True,
        ),
    ]
