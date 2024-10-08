from django.core.exceptions import ValidationError
from users.models import CustomUser
from django.db import models


class Event(models.Model):
    tilte = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    date = models.DateTimeField(blank=False, null=False)
    capacity = models.IntegerField(blank=False, null=False)
    organizer = models.ForeignKey(CustomUser, related_name='events',on_delete=models.CASCADE)

    def __str__(self):
        return self.tilte
    
    def clean(self):
        super().clean()  
        if self.organizer.role != 1 and self.organizer.role != 2:
            raise ValidationError('El usuario no tiene permiso para crear un evento.')

    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)


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
    rating = models.IntegerField(blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

