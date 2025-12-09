from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import Sign_Up_Form, AuthenticationForm, ProfileUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


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
            display_name = new_user.first_name if new_user.first_name else new_user.username
            messages.success(request, f"Account Created for {display_name}")
            return redirect("home")
    else:
        form = Sign_Up_Form()
    return render(request, "user/register.html", {"form": form})


def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request,"You already logged in 😊")
        return redirect("home")
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            display_name = user.first_name if user.first_name else user.username
            messages.success(request, f"Welcome Back Mr/Mrs {display_name}")
            login(request, user)
            return redirect("home")    
    else:
        form = AuthenticationForm()
    
    return render(request, "user/login.html", {"form": form})


def LogoutView(request):
    logout(request)
    return redirect("home")


@login_required
def ProfileView(request):
    
    if request.method == "POST":
        if "toggle_subscription" in request.POST:
            request.user.is_subscribed = not request.user.is_subscribed
            request.user.save()
            status = "Subscribed" if request.user.is_subscribed else "Unsubscribed"
            messages.success(request, f"You have successfully {status} to the newsletter.")
            return redirect("profile")
        
        elif "update_profile" in request.POST:
             form = ProfileUpdateForm(request.POST, instance=request.user)
             if form.is_valid():
                 form.save()
                 messages.success(request, "Your profile has been updated!")
                 return redirect("profile")
        
    form = ProfileUpdateForm(instance=request.user)
    return render(request, "user/profile.html", {"form": form})
