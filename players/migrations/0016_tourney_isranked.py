# Generated by Django 2.0.1 on 2018-01-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0015_auto_20180113_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourney',
            name='isRanked',
            field=models.BooleanField(default=True),
        ),
    ]
