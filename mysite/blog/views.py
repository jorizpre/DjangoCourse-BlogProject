from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin # Class needed in Class Based Views
from django.contrib.auth.decorators import login_required # decorator needed in Function Based Views
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy # waits to show the successfully deleted page until it is actually deleted
from django.utils import timezone


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


########################
# FUNCTIONAL VIEWS #
########################

# Comments Views (functional instead of Class Based View):

@login_required # convenience decorator to make login required for the view below (imported above)
def add_comment_to_post(request, pk): # pk links the comment to the post
    post = get_object_or_404(Post, pk=pk)
    if request.method =="POST": # if the form has been filled
        form = CommentForm(request.POST) # then pass the request
        if form.isvalid(): # if the form is valid and nothing is messed up
            comment = form.save(commit=False)
            comment.post = post # post is am attribute in the Comment class in our model
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/comment_form.html", {"form":form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve() # method of the Comment model
    return redirect("post_detail", pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk # as it is going to be deleted, we need to save it as a sepparate variable
    comment.delete()
    return redirect("post_detail", pk=post_pk)


# Publishing functional View

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish
    return redirect("post_detail", pk=pk)