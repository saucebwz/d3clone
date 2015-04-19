# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0004_auto_20150417_2353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='karma',
            old_name='username',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 17, 19, 56, 27, 888911, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 17, 19, 56, 27, 890911, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 17, 19, 56, 27, 887911, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
