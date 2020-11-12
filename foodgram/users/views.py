from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm, LoginForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "account/signup.html"


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "account/login.html", {"form": form})

        user = authenticate(request, **form.cleaned_data)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else:
                form.add_error("username", "Аккаунт отключен")
                return render(request, "account/login.html", {"form": form})
        else:
            form.add_error("username", "Неверный логин или пароль")
            return render(request, "account/login.html", {"form": form})
    form = LoginForm()
    return render(request, "account/login.html", {"form": form})
