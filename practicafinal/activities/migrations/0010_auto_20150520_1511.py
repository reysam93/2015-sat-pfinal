# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_auto_20150519_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(default=b'', max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='comments',
            field=models.ManyToManyField(to='activities.Comment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='selected',
            name='date',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpage',
            name='updated',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
