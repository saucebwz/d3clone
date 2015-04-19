# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0009_auto_20150418_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='karma',
            old_name='user',
            new_name='karma_user',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 4, 18, 16, 1, 54, 405808, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 18, 16, 1, 54, 407808, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 4, 18, 16, 1, 54, 404808, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
    ]
