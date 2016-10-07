# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(help_text=b'ID of the event (same as in Calendar42 API)', max_length=80, serialize=False, primary_key=True, db_index=True)),
                ('title', models.CharField(help_text=b'Event title', max_length=150)),
                ('participants', models.CharField(help_text=b'List of participants to the event', max_length=1500)),
                ('cache_date', models.DateTimeField(help_text=b"Datetime at which the event's data were last retrieved from the Calendar42 API", auto_now_add=True)),
            ],
        ),
    ]
