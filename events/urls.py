from django.urls import path
from .views import (
    EventCreateListView, 
    EventDetailUpdateDeleteView,
    RegisterEventView,
    CommentsEventCreateListView,
    CommentsEventDetailUpdateDeleteView,
    RatingsEventView
    )

urlpatterns = [
    # Events urls
    path('events/', EventCreateListView.as_view()),
    path('events/<int:event_id>/', EventDetailUpdateDeleteView.as_view()),
    # Register event url
    path('events/<int:event_id>/register/', RegisterEventView.as_view()),
    # Comments events urls
    path('events/<int:event_id>/comments/', CommentsEventCreateListView.as_view()),
    path('events/<int:event_id>/comments/<int:comment_id>/', CommentsEventDetailUpdateDeleteView.as_view()),
    # Rating envent url
    path('events/<int:event_id>/ratings/', RatingsEventView.as_view())
]

