from .views import (
    ProfileListRegistrationsView,
    ProfileView,
    RegisterUserView,
    LoginUserView,
    LogoutUserView
)
from django.urls import path

urlpatterns = [
    # Profile user urls
    path('profile/', ProfileView.as_view()),
    path('profile/registrations/', ProfileListRegistrationsView.as_view()),
    
    # Register, login and logout urls
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginUserView.as_view()),
    path('logout/', LogoutUserView.as_view()),
]
