from django import template
from dirty.models import Comment, Post
from django.shortcuts import get_object_or_404
register = template.Library()

@register.simple_tag
def get_likes_count(post_id):
    post = get_object_or_404(Post, pk=post_id)
    likes = post.like_set.filter(like=1).count()
    dislikes = post.like_set.filter(like=-1).count()
    result = likes - dislikes
    return str(result)

@register.inclusion_tag('comment_tree.html')
def com_tree(comment):
    children = Comment.objects.filter(parent=comment)
    return {'comment': comment, 'children': children}


@register.simple_tag
def get_comments_count(post_id):
    count = Comment.objects.filter(post__pk=post_id).count()
    if count > 0:
        string = str(Comment.objects.filter(post__pk=post_id).count()) + " комментария"
    else:
        return "0 комментариев"
    return string
