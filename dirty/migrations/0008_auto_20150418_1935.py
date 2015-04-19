# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0007_auto_20150418_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 4, 18, 15, 35, 33, 588390, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 18, 15, 35, 33, 591391, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='karma',
            name='user',
            field=models.OneToOneField(related_name='karma_children', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 4, 18, 15, 35, 33, 588390, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
    ]
