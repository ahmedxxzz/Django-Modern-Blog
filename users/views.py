from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import Sign_Up_Form
from django.contrib.auth import login


# Create your views here.
def Sign_Up_View(request):
    if request.user.is_authenticated:
        messages.warning(
            request, f"You already have an account Mr {request.user.username}"
        )
        return redirect("home")
    if request.method == "POST":
        form = Sign_Up_Form(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, f"Account Created for {new_user.username}")
            return redirect("home")
    else:
        form = Sign_Up_Form()
    return render(request, "user/register.html", {"form": form})
