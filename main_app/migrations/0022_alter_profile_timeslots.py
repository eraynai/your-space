# Generated by Django 3.2.4 on 2021-07-15 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_merge_0013_auto_20210715_1434_0020_auto_20210715_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='timeslots',
            field=models.ManyToManyField(to='main_app.Timeslot'),
        ),
    ]
