# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0006_auto_20150417_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 18, 15, 26, 23, 9899, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 18, 15, 26, 23, 15899, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='karma',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='karma_children', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 18, 15, 26, 23, 8899, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
