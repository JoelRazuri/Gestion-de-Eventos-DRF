from .views import EventCreateListView, EventDetailUpdateDeleteView
from django.urls import path

urlpatterns = [
    path('events/', EventCreateListView.as_view()),
    path('events/<int:pk>', EventDetailUpdateDeleteView.as_view()),
]

