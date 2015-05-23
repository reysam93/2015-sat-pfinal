# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=150)),
                ('type', models.CharField(default=b'', max_length=300)),
                ('price', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(default=datetime.date(1, 1, 1))),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('long', models.BooleanField(default=False)),
                ('url', models.CharField(default=b'', max_length=300)),
            ],
            options={
                'ordering': ['date', 'time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCSS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bgCont', models.CharField(default=b'white', max_length=30)),
                ('bgBanner', models.CharField(default=b'black', max_length=30)),
                ('bgCopyRigth', models.CharField(default=b'white', max_length=30)),
                ('bgLogBox', models.CharField(default=b'#999999', max_length=30)),
                ('bgMenu', models.CharField(default=b'black', max_length=30)),
                ('wordColorCont', models.CharField(default=b'black', max_length=30)),
                ('wordColorBanner', models.CharField(default=b'black', max_length=30)),
                ('wordColorCopyRigth', models.CharField(default=b'black', max_length=30)),
                ('wordColorLogBox', models.CharField(default=b'black', max_length=30)),
                ('wordColorMenu', models.CharField(default=b'#999999', max_length=30)),
                ('wordSizeCont', models.IntegerField(default=10)),
                ('wordSizeBanner', models.IntegerField(default=10)),
                ('wordSizeCopyRigth', models.IntegerField(default=10)),
                ('wordSizeLogBox', models.IntegerField(default=10)),
                ('wordSizeMenu', models.IntegerField(default=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(default=b'', max_length=30)),
                ('title', models.CharField(default=b'', max_length=50)),
                ('nActs', models.IntegerField(default=0)),
                ('description', models.TextField(default=b'')),
                ('updated', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0), auto_now=True)),
                ('acts', models.ManyToManyField(to='activities.Activity')),
                ('css', models.ForeignKey(default=None, to='activities.UserCSS')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
