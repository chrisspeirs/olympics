# Generated by Django 2.0.1 on 2018-01-13 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0014_auto_20180111_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourney',
            name='name',
            field=models.CharField(default='Bowling', max_length=50),
        ),
    ]
