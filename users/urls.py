from .views import (
    UserListView, 
    UserDetailView, 
    UserListRegistrationsView, 
    ProfileListRegistrationsView,
    ProfileView
)
from django.urls import path

urlpatterns = [
    # Users urls for administration
    path('users/', UserListView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view()),
    path('users/<int:user_id>/registrations/', UserListRegistrationsView.as_view()),
    # Profile user urls
    path('profile/', ProfileView.as_view()),
    path('profile/registrations/', ProfileListRegistrationsView.as_view()),
]
