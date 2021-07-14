# Generated by Django 3.2.4 on 2021-07-14 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_rename_profile_photo_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='buddy',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='timeSlot',
        ),
        migrations.AddField(
            model_name='profile',
            name='timeslots',
            field=models.ManyToManyField(to='main_app.Timeslot'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
