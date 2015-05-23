# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0008_auto_20150519_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selected',
            name='id',
        ),
        migrations.AlterField(
            model_name='selected',
            name='act',
            field=models.ForeignKey(primary_key=True, serialize=False, to='activities.Activity'),
            preserve_default=True,
        ),
    ]
