# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0004_auto_20150518_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpage',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='userpage',
            name='whoLikes',
        ),
        migrations.AddField(
            model_name='activity',
            name='likes',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='whoLikes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
