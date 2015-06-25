from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404

class PopularPostManager(models.Manager):
    def get_queryset(self):
        query_set = super(PopularPostManager, self).get_queryset()
        posts = Post.objects.annotate(num=Sum('likes__like')).order_by('-num')
        return posts

class Post(models.Model):
    user = models.ForeignKey('DirtyUser')
    title = models.CharField(default="", max_length=100)
    description = models.TextField(default="")
    created_on = models.DateField(auto_now_add=True)
    is_gold = models.BooleanField(default=False)

    def __str__(self):
        return self.title





class Comment(models.Model):
    post = models.ForeignKey(Post)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    author = models.ForeignKey('DirtyUser')
    text = models.CharField(default="", null=True, blank=True, max_length=1000)
    created_on = models.DateField(auto_now_add=True)
    isNotChild = models.BooleanField(default=True)
    head = models.IntegerField(default=0)



    def __str__(self):
        return "Comment№ " + str(self.id)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', default=0)
    user = models.ForeignKey('DirtyUser')
    like = models.IntegerField(default=0)
    objects = models.Manager()
    popular_posts = PopularPostManager()

    def __str__(self):
        return "{0} is liked or disliked {1}".format(self.user.username, self.post.title)


"""
class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    born = models.DateField(default=timezone.now())
    about = models.CharField(default="", blank=True, max_length=200)
"""


class DirtyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None,  **kwargs):
        now = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email, date_joined=now, is_superuser=False, is_staff=False, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        u = self.create_user(username, email, password, **kwargs)
        u.is_superuser = True
        u.is_staff = True
        u.save(using=self._db)
        return u


class Favorites(models.Model):
    post = models.ForeignKey('Post', related_name='favorites')
    user = models.ForeignKey('DirtyUser')


class KarmaWVL(models.Model):
    who_added = models.ForeignKey('DirtyUser')
    count = models.IntegerField(default=0)
    voted = models.ForeignKey('Karma', related_name='voted_users', null=True)


class Karma(models.Model):
    karma_user = models.OneToOneField('DirtyUser')
    count = models.IntegerField(default=0)


class DirtyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    second_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    about = models.CharField(blank=True, max_length=1500)



    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = DirtyUserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return ', '.join((self.first_name, self.second_name))