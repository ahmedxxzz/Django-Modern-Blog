from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post


# Create your views here.
def home(request):
    post_list = Post.objects.filter(status=1).order_by("author")
    paginator = Paginator(post_list, 3)  # Show 5 posts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/home.html", {"page_obj": page_obj})


def post_details(request, slug):
    post_detail = get_object_or_404(Post, status=1, slug=slug)
    return render(request, "blog/post_detail.html", {"post_detail": post_detail})
