# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20150518_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercss',
            name='bgBanner',
            field=models.CharField(default=b'white', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeBanner',
            field=models.PositiveIntegerField(default=25),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeCont',
            field=models.PositiveIntegerField(default=12),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeCopyRigth',
            field=models.PositiveIntegerField(default=12),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeLogBox',
            field=models.PositiveIntegerField(default=12),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeMenu',
            field=models.PositiveIntegerField(default=15),
            preserve_default=True,
        ),
    ]
