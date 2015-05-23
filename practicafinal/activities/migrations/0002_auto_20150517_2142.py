# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpage',
            name='acts',
            field=models.ManyToManyField(default=None, to='activities.Activity'),
            preserve_default=True,
        ),
    ]
