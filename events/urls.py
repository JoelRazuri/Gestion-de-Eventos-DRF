from django.urls import path
from .views import (
    EventCreateListView, 
    EventDetailUpdateDeleteView,
    RegisterForEventView
    )

urlpatterns = [
    path('events/', EventCreateListView.as_view()),
    path('events/<int:pk>', EventDetailUpdateDeleteView.as_view()),
    path('events/<int:event_id>/register/', RegisterForEventView.as_view()),
]

