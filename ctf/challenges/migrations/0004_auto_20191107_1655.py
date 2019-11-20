# Generated by Django 2.2.6 on 2019-11-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_challengetype_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='points',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='challengetype',
            name='points',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
