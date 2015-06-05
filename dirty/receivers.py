from django.dispatch import receiver
from django.db.models.signals import post_save
from dirty.templatetags.tags import get_likes_count
from dirty.signals import post_liked, karma_inited
from dirty.models import DirtyUser, Karma
from django.shortcuts import get_object_or_404


@receiver(post_liked)
def handle_post_viewed(sender, **kwargs):
    post = sender
    likes = get_likes_count(sender.id)
    if int(likes) + 1 >= 2:
        post.is_gold = True
    post.save()


@receiver(karma_inited)
def init_karma(sender, **kwargs):
    karma = Karma(karma_user=sender, count=0)
    karma.save()