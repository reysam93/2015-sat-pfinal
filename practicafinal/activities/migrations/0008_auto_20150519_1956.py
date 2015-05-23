# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20150519_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selected',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now=True)),
                ('act', models.ForeignKey(to='activities.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userpage',
            name='acts',
        ),
        migrations.AddField(
            model_name='userpage',
            name='selected',
            field=models.ManyToManyField(to='activities.Selected'),
            preserve_default=True,
        ),
    ]
