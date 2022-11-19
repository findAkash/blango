from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from blog.forms import CommentForm
import logging

#creating a model level variable
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                #save the form, using the commit=False argument. This won’t write the Comment object to the database, instead it will return it. We need to do this to set the other attributes on the Comment before saving.
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                # refresh the page for the user to so they see their new comment
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})