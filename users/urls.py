from .views import UserListView, UserDetailView, ListUserRegistrationsView
from django.urls import path

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view()),
    path('users/registrations/', ListUserRegistrationsView.as_view())
]
