# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0002_auto_20150408_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='dirtyuser',
            name='karma',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 4, 15, 23, 41, 47, 133372, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 15, 23, 41, 47, 134372, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 4, 15, 23, 41, 47, 133372, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
    ]
