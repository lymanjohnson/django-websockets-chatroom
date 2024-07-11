from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("<str:room_name>/", views.room, name="room"),
]