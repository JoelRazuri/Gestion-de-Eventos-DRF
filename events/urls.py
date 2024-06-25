from .views import EventCreateListView, EventDetailUpdateDeleteView
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

urlpatterns = [
    path('events/', EventCreateListView.as_view()),
    path('events/<int:pk>', EventDetailUpdateDeleteView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)