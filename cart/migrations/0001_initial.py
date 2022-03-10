# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
        ('df_goods', '0002_auto_20180421_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=1, max_length=20)),
                ('goods', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('use', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
    ]
