from django import template
from dirty.models import Comment, Post, Like, Favorites, CommentRead
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Sum
register = template.Library()


@register.simple_tag
def get_likes_count(post_id):
    likes = Like.objects.filter(post__id=post_id)
    #post = get_object_or_404(Post, pk=post_id)
    positive_likes = likes.filter(like=1).count()
    dislikes = likes.filter(like=-1).count()
    result = positive_likes - dislikes
    return str(result)


@register.simple_tag
def is_favourite(post_id, user):

    if Favorites.objects.filter(user=user, post__pk=post_id).exists():
        return "<b>***</b>"
    else:
        return "***"


@register.simple_tag
def is_newcomments(post_id, user):

    _read_comments = CommentRead.objects.filter(post__pk=post_id, user=user).count()
    all_comments = Comment.objects.filter(post__pk=post_id).count()
    if _read_comments < all_comments:
        return True
    else:
        return False



@register.inclusion_tag('comment_tree.html')
def com_tree(comment):
    children = Comment.objects.filter(parent=comment)
    return {'comment': comment, 'children': children}


@register.inclusion_tag('build_post.html')
def build_post(post_id, user=None):
    _p = get_object_or_404(Post, pk=post_id)
    return {'item': _p, 'user': user}


@register.simple_tag
def get_comments_count(post_id):
    count = Comment.objects.filter(post__pk=post_id).count()
    if count > 0:
        string = str(Comment.objects.filter(post__pk=post_id).count()) + " комментария"
    else:
        return "0 комментариев"
    return string

@register.simple_tag
def get_full_info_about_post(post_id, user):
        new_comments = is_newcomments(post_id, user)
        if new_comments:
            pre, suf = "<b>", "</b>"
        else:
            pre, suf = "", ""

        count = get_comments_count(post_id)
        post = get_object_or_404(Post, pk=post_id)
        url = reverse("profile_view", args=(post.user.username, ))
        return "Написал <a href={0}>{1}</a> в {2}, {4}{3}{5}".format(url, post.user.username, post.created_on, count, pre, suf)