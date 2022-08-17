from django.urls import path

from . import views

urlpatterns = [
    
    path("new/", views.post_new, name="post_new"),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path("<username>/<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("group/<slug:slug>/", views.group_posts, name="group"),
    
    path("<username>/<int:post_id>/comment/", views.comment_add, name="comment_add"),
    path("<username>/<int:post_id>/comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
    
    path('<str:username>/', views.profile, name='profile'),
    path("<username>/edit/", views.profile_edit, name="profile_edit"),
    path("follow/", views.follow_index, name="follow"),
    path("<username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    
    path('404', views.page_not_found),
    path('500', views.server_error),
    
    path("", views.index, name="index"),
]
