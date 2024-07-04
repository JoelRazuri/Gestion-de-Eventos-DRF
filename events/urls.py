from django.urls import path
from .views import (
    EventCreateListView, 
    EventDetailUpdateDeleteView,
    RegisterEventView,
    CommentsEventCreateListView
    )

urlpatterns = [
    path('events/', EventCreateListView.as_view()),
    path('events/<int:event_id>/', EventDetailUpdateDeleteView.as_view()),
    path('events/<int:event_id>/register/', RegisterEventView.as_view()),
    path('events/<int:event_id>/comments/', CommentsEventCreateListView.as_view()),
    path('events/<int:event_id>/comments/<int:comment_id>/', CommentsEventCreateListView.as_view()),
    
    # path('events/<int:event_id>/rating/', RegisterEventView.as_view())
]

