from django.shortcuts import render
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin # Class needed in Class Based Views
# from django.contrib.auth.decorators import login_required # decorator needed in Function Based Views
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy # waits to show the successfully deleted page until it is actually deleted



class PostListView(ListView):
    """This will be our Home Page: a list of the existing blog posts
    """    
    model = Post

    def get_queryset(self):
        """Django ORM (Object Relational Mapper):
        Sort of doing a SQL query to our Django models.
        Grabbing the Post Model and filtering it with the conditions below.
        """        
        return Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")
        # concretamente: grabbing the "published date", 
        # "lte= less than or equal to" the current time (more info, under "Field Lookups": https://docs.djangoproject.com/en/4.2/topics/db/queries/)
        # and order them by the inverse of the published date (most recent on top)


class AboutView(TemplateView):
    template_name = "about.html"

class PostDetailView(DetailView):
    """Page to see the details of a specific Post
    """
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    """Page to create posts, which should only be available for logged users

    """    
    # Required variables for inherited "CreateView"
    form_class = PostForm
    model = Post
    
    # Required variables for inherited LoginRequiredMixin
    login_url = "/login/" # where the user is forwarded when they need to log in
    redirect_field_name = "blog.post_detail.html" # redirected after login to

class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Page to edit posts, which should also only be available for logged users

    """  
    form_class = PostForm
    model = Post
    login_url = "/login/"
    redirect_field_name = "blog.post_detail.html"

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """View to delete certain posts
    """    
    model = Post
    success_url = reverse_lazy("post_list") # to go back to the home page after deleting

class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    login_url = "/login/"
    redirect_field_name = "blog/post_list.html"

    def get_queryset(self):
        """In this case, we want to show all existing posts, not only the published ones
        """        
        return Post.objects.filter(published_date__isnull=True).order_by("-created_date")