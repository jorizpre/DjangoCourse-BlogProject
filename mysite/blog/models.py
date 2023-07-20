from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User') # the authors will be the superusers (we will change that later for a multiuser approach)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True,null=True) # can be left blank or chosen as null (no publication date whatsoever)

    def publish(self):
        """Basically this method gives the option to edit the publishing date
        (not needed for the create_date variable, which will just be created automatically once)
        """        
        self.pulished_date = timezone.now()
        self.save()

    def approve_comments(self):
        """This will allow us to select the approved comments and show them in the website
        """        
        return self.comments.filter(approved_comment=True)

    def get_absolute_url():
        """Needed for Class Based Views (CBV): once the post or comment is created, it tells the website where to go back to
        """       
        return reverse("post_detail", kwargs={"pk":self.pk})

    def __str__(self):
        """String representation of the model
        """        
        return self.title

class Comment(model.Model):
    """
    """
    post = models.ForeignKey("blog.Post", related_name="comments") # to link each comment to a post
    author = models.CharField(max_length=200) # free input (no user required)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)
    
    def approve(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text


    
