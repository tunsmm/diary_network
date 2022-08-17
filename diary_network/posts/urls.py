from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.group_posts, name="group_post"),
    path("new/", views.post_new, name="post_new"),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    
    path("<username>/<int:post_id>/comment/", views.comment_add, name="comment_add"),
    path("<username>/<int:post_id>/comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
    path('404', views.page_not_found),
    path('500', views.server_error)
]
