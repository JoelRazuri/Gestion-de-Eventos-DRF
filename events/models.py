from django.db import models
from users.models import CustomUser
from .validations import *


class Event(models.Model):
    tilte = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='event_images/')
    date = models.DateTimeField(validators=[validator_is_valid_date], blank=False, null=False)
    capacity = models.IntegerField(validators=[validator_capacity], blank=False, null=False)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, validators=[validator_is_organizer])


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[validator_rating], blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

