from .views import (
    ProfileListRegistrationsView,
    ProfileView,
    RegisterUserView,
    LoginUserView,
    LogoutUserView,
    ListUsersView
)
from django.urls import path

urlpatterns = [
    # Profile user urls
    path('user/profile/', ProfileView.as_view()),
    path('user/profile/registrations/', ProfileListRegistrationsView.as_view()),
    
    # Register, login and logout urls
    path('user/register/', RegisterUserView.as_view()),
    path('user/login/', LoginUserView.as_view()),
    path('user/logout/', LogoutUserView.as_view()),

    # List users for Administrators
    path('users/', ListUsersView.as_view())
]
