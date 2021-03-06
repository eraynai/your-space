from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.


class Timeslot(models.Model):
    date = models.DateField()
    slot = models.CharField(max_length=50)
    class Meta:
        ordering = ['date']
        
    def __str__(self):
        return self.slot
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timeslots = models.ManyToManyField(Timeslot)
    role = models.CharField(max_length=50)
    bio = models.TextField(max_length=250)
    linkedin = models.CharField(max_length=50)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    #

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    #

    def __str__(self):
        return self.user.username




class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.user_id} @{self.url}"
