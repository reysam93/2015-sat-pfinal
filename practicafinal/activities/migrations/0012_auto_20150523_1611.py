# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0011_auto_20150520_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selected',
            name='date',
            field=models.DateField(default=datetime.date(1, 1, 1)),
            preserve_default=True,
        ),
    ]
