from .models import Event, Registration, Comment, Rating
from django.contrib import admin

# Register models Event, Registration, Comment and Rating in administration of Django
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Comment)
admin.site.register(Rating)