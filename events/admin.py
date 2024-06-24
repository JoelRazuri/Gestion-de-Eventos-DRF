from django.contrib import admin
from .models import Event, Registration, Comment, Rating


admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Comment)
admin.site.register(Rating)