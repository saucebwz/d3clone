# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0008_auto_20150418_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 18, 15, 42, 10, 17065, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 18, 15, 42, 10, 20065, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='karma',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 18, 15, 42, 10, 17065, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
