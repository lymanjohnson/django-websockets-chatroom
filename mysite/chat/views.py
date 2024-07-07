from django.conf import settings
from django.shortcuts import render, redirect, reverse
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import FormView


# class SignupView(FormView):
#     template_name = "registration/signup.html"
#     form_class = UserCreationForm
#     success_url = "/chat/"

def logout_view(request):
    logout(request)
    return redirect("/chat/login/")

def signup(request):
    logout(request)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticate(new_user)
            return redirect("/chat/")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


def index(request):
    if request.user.is_authenticated:
        return render(request, "chat/index.html")
    else:
        return redirect(f"{reverse('chat:login')}?next={request.path}")


def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, "chat/room.html", {"room_name": room_name})
    else:
        return redirect(f"{reverse('chat:login')}?next={request.path}")