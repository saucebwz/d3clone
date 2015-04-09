from django.dispatch import receiver
from dirty.templatetags.tags import get_likes_count
from dirty.signals import post_liked

@receiver(post_liked)
def handle_post_viewed(sender, **kwargs):
    post = sender
    likes = get_likes_count(sender.id)
    if int(likes) + 1 >= 2:
        post.is_gold = True
    post.save()