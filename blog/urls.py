from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("post/<slug:slug>", post_details, name="post_detail"),
    path("post/<int:post_id>/like", post_like, name="toggle_like"),
    path("tag/<slug:tag_slug>/", post_by_tag, name="post_by_tag"),
    path("subscribe/", Subscribe_View, name="subscribe"),
    path("search/", Search_View, name="search"),
]
