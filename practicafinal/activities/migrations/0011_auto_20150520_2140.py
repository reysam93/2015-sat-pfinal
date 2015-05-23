# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_auto_20150520_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='nick',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
    ]
