import logging
from django.contrib.auth import get_user_model
from django import template
from django.utils.html import format_html

user_model = get_user_model()
register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def author_details(author, current_user=None):
    print("current user = ", current_user)
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag
def row(extra_classes=""):
  return format_html('<div class="row">', extra_classes)

@register.simple_tag
def endrow():
  return format_html("</div>")

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col">', extra_classes)

@register.simple_tag
def endcol():
    return format_html('</div>')

@register.simple_tag(takes_context=True)
def author_details_tag(context):
    request = context["request"]
    current_user = request.user
    post = context["post"]
    logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
    author = post.author

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html("{}{}{}", prefix, name, suffix)