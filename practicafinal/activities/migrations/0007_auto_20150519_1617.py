# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_auto_20150519_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercss',
            name='wordColorBanner',
            field=models.CharField(default=b'#778899', max_length=30),
            preserve_default=True,
        ),
    ]
