from django import forms
from blog.models import Post, Comment # importing the created models

class PostForm(forms.ModelForm):
    
    class Meta():
        """Class to be used to create widget-specific properties
        """        
        model = Post
        fields = ("author", "title", "text")

        # Connecting widgets to CSS classes ("textinputclass" and "postcontent" are ours, the others are not):
        widgets = {
            "title":forms.TextInput(attrs={"class":"textinputclass"}),
            "text":forms.Textarea(attrs={"class":"editable medium-editor-textarea postcontent"})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ("author", "text")

        widgets={
            "author":forms.TextInput(attrs={"class":"textinputclass"}),
            "text":forms.Textarea(attrs={"class":"editable medium-editor-textarea"})
        }
