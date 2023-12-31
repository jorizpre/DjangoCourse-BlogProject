from django.urls import path
from blog import views # we could also say "from . import views" as we are placed in the same path

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'), # as_view() method needed for Class Based Views
    path('about/', views.AboutView.as_view(), name='about'), # this is done different in the tutorial "video 168" (might be worth checking)
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/new/", views.CreatePostView.as_view(), name="post_new"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/remove/", views.PostDeleteView.as_view(), name="post_remove"),
    path("drafts/", views.DraftListView.as_view(), name="post_draft_list"),
    path("post/<int:pk>/comment/", views.add_comment_to_post, name="add_comment_to_post"), # functional based view
    path("comment/<int:pk>/approve/", views.comment_approve, name="comment_approve"),
    path("comment/<int:pk>/remove/", views.comment_remove, name="comment_remove"),
    path("post/<int:pk>/publish/", views.post_publish, name="post_publish"),

 ]


