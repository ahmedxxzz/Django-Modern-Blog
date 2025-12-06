from django.urls import path
from .views import *


urlpatterns = [
    path("register/", Sign_Up_View, name="register"),
]
