
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_post', views.create_post, name='create_post'),
    path("profile/<str:username>", views.profile, name="profile"),
     path("following", views.following, name="following"),

    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path('update_post/<int:post_id>', views.update_post, name='update_post'),
    path('remove_like/<int:post_id>', views.remove_like, name='remove_like'),
    path('add_like/<int:post_id>', views.add_like, name='add_like'),

]
