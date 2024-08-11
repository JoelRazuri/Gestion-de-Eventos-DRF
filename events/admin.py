from .models import Event, Registration, Comment, Rating
from django.contrib import admin


admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Comment)
admin.site.register(Rating)