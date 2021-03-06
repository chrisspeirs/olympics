# Generated by Django 2.0.1 on 2018-01-11 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0011_auto_20171222_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=0)),
                ('player', models.ForeignKey(null=True, on_delete='cascade', related_name='playerr', to='players.Players')),
                ('tourney', models.ForeignKey(null=True, on_delete='cascade', related_name='olympic1', to='players.Tourney')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together={('player', 'tourney')},
        ),
    ]
