from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("post/<slug:slug>", post_details, name="post_detail"),
    path("subscribe/", Subscribe_View, name="subscribe"),
]
