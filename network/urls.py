
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # post to the post route make a new post
    path("post", views.post, name="post"),
    path("getPost/<str:section>", views.getPosts, name="getPosts"),
    path("getUser/<str:userID>", views.getUser, name="getUser"),
    path("getSelf", views.getSelf, name = "getSelf"),
    path("getUserPosts/<str:user>", views.getUserPosts, name="getUserPost"),
    path("likePost/<int:postID>", views.likePost, name="likePost"),
    path("editPost/<int:post>", views.editPost, name="editPost"),
    path("followUser/<str:name>", views.followUser, name="followUser"),
    path("doesFollow/<str:selectedUser>", views.doesFollow, name="doesFollow")
]