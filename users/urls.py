from .views import (
    UserListView, 
    UserDetailView, 
    UserListRegistrationsView, 
    ProfileListRegistrationsView,
    ProfileView,
    RegisterUserView,
    LoginUserView,
    LogoutUserView
)
from django.urls import path

urlpatterns = [
    # Users urls for administration
    path('users/', UserListView.as_view()),
    path('users/<int:user_id>', UserDetailView.as_view()),
    path('users/<int:user_id>/registrations/', UserListRegistrationsView.as_view()),
    # Profile user urls
    path('profile/', ProfileView.as_view()),
    path('profile/registrations/', ProfileListRegistrationsView.as_view()),
    # Register and Login urls
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginUserView.as_view()),
    path('logout/', LogoutUserView.as_view()),
]
