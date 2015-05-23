# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0003_auto_20150518_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpage',
            name='likes',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpage',
            name='whoLikes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeBanner',
            field=models.PositiveIntegerField(default=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeCont',
            field=models.PositiveIntegerField(default=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeCopyRigth',
            field=models.PositiveIntegerField(default=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeLogBox',
            field=models.PositiveIntegerField(default=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercss',
            name='wordSizeMenu',
            field=models.PositiveIntegerField(default=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpage',
            name='nActs',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
