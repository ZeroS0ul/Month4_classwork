from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход сразу после создания аккаунта
            return redirect("post_list")  # Имя вашего URL-маршрута главной страницы
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})