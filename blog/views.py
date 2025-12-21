from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post, Comment, Like, Tag
from .forms import CommentForm, NewsSubscriberForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

# Create your views here.
@cache_page(60 * 15)
@vary_on_cookie
def home(request):
    post_list = Post.objects.filter(status=1).select_related("author").order_by("author")
    paginator = Paginator(post_list, 3)  # Show 5 posts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/home.html", {"page_obj": page_obj})


@cache_page(60 * 15)
@vary_on_cookie
def post_details(request, slug):
    post_detail = get_object_or_404(
        Post.objects.select_related("author").prefetch_related("tags"), 
        status=1, 
        slug=slug
    )
    comments = post_detail.comments.select_related("author").all()
    user_comment = None

    is_liked = False
    if request.user.is_authenticated:
        is_liked = post_detail.likes.filter(user=request.user).exists()

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
        "comment_form": comment_form,
        "is_liked": is_liked
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

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=1)
    like,created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    like_count = post.likes.count()
    return JsonResponse({"liked": liked, "like_count": like_count})


def post_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    post_list = Post.objects.filter(status=1, tags=tag).select_related("author").order_by("author")
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/home.html", {"page_obj": page_obj, "tag": tag})


def Search_View(request):
    query = request.GET.get('q')
    results = Post.objects.none()
    if query:
        results = Post.objects.filter( Q(title__icontains=query) | Q(content__icontains=query) ).select_related("author").distinct()
    
    paginator = Paginator(results, 3)
    page_obj = paginator.get_page(request.GET.get("page"))
    
    return render(request, "blog/home.html", {'query': query, 'page_obj': page_obj})
