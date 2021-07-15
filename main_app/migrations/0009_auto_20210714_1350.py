# Generated by Django 3.2.4 on 2021-07-14 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_profile_timeslots'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='profile',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='profile',
            name='timeslots',
            field=models.ManyToManyField(to='main_app.Timeslot'),
        ),
    ]