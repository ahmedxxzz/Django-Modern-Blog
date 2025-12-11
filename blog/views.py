from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm, NewsSubscriberForm
from users.models import CustomUser


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


def Subscribe_View(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        form = NewsSubscriberForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if email belongs to an existing user
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, 'This email is already registered. Please login to manage your subscription.')
                return redirect('login')
            form.save()
            messages.success(request, 'You have successfully subscribed to our newsletter!')
            return redirect('home')
    else:
        form = NewsSubscriberForm()
        
    return render(request, "blog/subscribe.html", {"form": form})
