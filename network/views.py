from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    if request.user.is_authenticated:
        # Retrieve all posts from the database and order them by creation date in descending order
        posts = Post.objects.all().order_by('-created_at')
        paginator = Paginator(posts, 10)  # Show 10 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {"page_obj": page_obj})
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def following(request):
    following_users = request.user.following.all()
    all_posts = []
    for user in following_users:
        posts = user.posts.all()
        all_posts.extend(posts)
    # Sort `all_posts` by the 'created_at' field in descending order (latest first)
    all_posts = sorted(all_posts, key=lambda post: post.created_at, reverse=True)
    return render(request, "network/index.html", {'posts': all_posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@csrf_exempt
@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')

        if content.strip():
                # Save the post to the database
                new_post = Post(user=request.user, content=content)
                new_post.save()

                return JsonResponse({'message': 'Post created successfully'})
        else:
            return JsonResponse({'message': 'Post content is empty'}, status=400)
        
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@login_required
def profile(request, username):
    # Retrieve the user with the provided username or return a 404 error if not found
    # user = get_object_or_404(User, username=username)
    current_user = request.user
    profile_user = User.objects.get(username=username)
    followers = profile_user.followers.all() 
    following = profile_user.following.all()
    posts_for_specific_user = Post.objects.filter(user__username=username).order_by('-created_at')
    print(posts_for_specific_user)
    return render(request, "network/profile.html",{
        'profile_user': profile_user,
        'current_user': current_user, 
        'followers': followers, 
        'following': following, 
        'posts': posts_for_specific_user})

@csrf_exempt
@login_required
def follow(request, username):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    user_to_follow = User.objects.get(username=username)
    request.user.following.add(user_to_follow)
    data = {
        'message': 'You are now following ' + username,
        'redirect_url': reverse('profile', args=[username])
    }
    json_response = JsonResponse(data)
    return json_response

@csrf_exempt
@login_required
def unfollow(request, username):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    user_to_unfollow = User.objects.get(username=username)
    request.user.following.remove(user_to_unfollow)
    # Create a dictionary containing the message and redirect URL
    data = {
        'message': 'You have unfollowed ' + username,
        'redirect_url': reverse('profile', args=[username])
    }
    json_response = JsonResponse(data)
    return json_response


