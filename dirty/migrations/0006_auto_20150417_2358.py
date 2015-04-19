# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0005_auto_20150417_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 17, 19, 58, 23, 844544, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 17, 19, 58, 23, 847544, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='karma',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='karma_children'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 17, 19, 58, 23, 844544, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
