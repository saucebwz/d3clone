# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dirty', '0003_auto_20150416_0341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Karma',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('count', models.IntegerField(default=0)),
                ('username', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='dirtyuser',
            name='about',
        ),
        migrations.RemoveField(
            model_name='dirtyuser',
            name='karma',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 17, 19, 53, 34, 423990, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dirtyuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 17, 19, 53, 34, 425990, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 4, 17, 19, 53, 34, 422990, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
