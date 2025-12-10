from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post,Comment
from .forms import CommentForm

# Create your views here.
def home(request):
    post_list = Post.objects.filter(status=1).order_by("author")
    paginator = Paginator(post_list, 3)  # Show 5 posts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/home.html", {"page_obj": page_obj})


def post_details(request, slug):
    post_detail = get_object_or_404(Post, status=1, slug=slug)
    comments = post_detail.comments.all()
    user_comment = None

    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.post = post_detail
                user_comment.author = request.user
                user_comment.save()
                return redirect('post_detail', slug=post_detail.slug)
        else:
            return redirect('login') 
    else:
        comment_form = CommentForm()
        
    return render(request, "blog/post_detail.html", {
        "post_detail": post_detail, 
        "comments": comments, 
        "comment_form": comment_form
    })