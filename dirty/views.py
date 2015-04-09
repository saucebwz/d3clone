from django.shortcuts import render
from django.views import generic
from django.views import generic
from django.shortcuts import render_to_response
from django.views.generic import View
from dirty.models import Post, Like, DirtyUser, Comment
from dirty.forms import PostForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from dirty.forms import DirtyUserProfileForm, DirtyUserForm, CommentForm
from dirty.mixins import LoginRequiredMixin
from dirty.signals import post_liked
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User




class MainView(generic.ListView):
    model = Post
    template_name = "main.html"
    context_object_name = "list_popular_posts"

    def get_queryset(self):
        return Post.objects.all()


class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = DirtyUserForm

    def post(self, request, *args, **kwargs):
        form = DirtyUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main_view'))
        else:
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

    def get_success_url(self):
        return reverse('main_view')


class LoginView(View):

    def get(self, request):
        return render_to_response('login.html', context_instance=RequestContext(request))

    def post(self, request):
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('main_view'))
        return render_to_response('login.html', {},
                              context_instance=RequestContext(request))


@login_required(login_url=reverse_lazy('login_view'))
def like_the_post(request, post_id):
    like_int = 1 if request.POST['submit'] == '+' else -1
    post = get_object_or_404(Post, pk=post_id)
    post_likes, created = post.like_set.get_or_create(user=request.user)
    if created:
        post_likes.like = like_int
        post_liked.send(sender=post)
        post_likes.save()
        return HttpResponseRedirect(reverse('main_view'))
    if post_likes:
        if post_likes.like != like_int:
            post_likes.like = like_int
            post_liked.send(sender=post)
            post_likes.save()
            return HttpResponseRedirect(reverse('main_view'))
        else:
            post_likes.like = 0
            post_liked.send(sender=post)
            post_likes.save()
            return HttpResponseRedirect(reverse('main_view'))
    else:
        new_like = Like(user=request.user, post=post, like=like_int)
        post_liked.send(sender=post)
        new_like.save()
        return HttpResponseRedirect(reverse('main_view'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main_view'))


class NewPost(generic.FormView):
    template_name = "newpost.html"
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse('main_view'))


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, profile_name):
        user = get_object_or_404(DirtyUser, username=profile_name)
        about = user.about
        isOwn = False
        if request.user.username == user.username:
            isOwn = True
        return render_to_response("profile.html", {'about': about, 'isOwn': isOwn}, context_instance=RequestContext(request))


class ProfileEdit(LoginRequiredMixin, generic.FormView):
    template_name = "profile_edit.html"
    form_class = DirtyUserProfileForm

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.about = request.POST['about']
        user.second_name = request.POST['second_name']
        user.save()
        return render_to_response('main.html', {}, context_instance=RequestContext(request))


    def get_initial(self):
        username = self.request.user.username
        email = self.request.user.email
        first_name = self.request.user.first_name
        second_name = self.request.user.second_name
        about = self.request.user.about
        return {'username': username, 'email': email, 'first_name': first_name, 'second_name': second_name, 'about': about}


class PostView(View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm()
        comments = post.comment_set.all()
        return render_to_response('post.html', {'post': post, 'form': form, 'comments': comments}, context_instance=RequestContext(request))

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comment_set.all()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_view", args=(post_id, )))
        else:
            return render_to_response("post.html", {'post': post, 'form': form, 'comments': comments}, context_instance=RequestContext(request))

def answer_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    postdata = request.POST.copy()
    comment_text = postdata['comment-text']
    new_comment = Comment(post=comment.post, parent=comment, author=request.user, text=comment_text, isNotChild=False)
    new_comment.save()
    return HttpResponseRedirect(reverse("post_view", args=(comment.post.id, )))