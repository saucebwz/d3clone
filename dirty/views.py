from django.shortcuts import render
from django.views import generic
from django.views import generic
from django.shortcuts import render_to_response
from django.views.generic import View
from dirty.models import Post, Like, DirtyUser, Comment, Karma, KarmaWVL, Favorites
from dirty.forms import PostForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from dirty.forms import DirtyUserProfileForm, DirtyUserForm, CommentForm
from dirty.mixins import LoginRequiredMixin
from dirty.signals import post_liked, karma_inited
from dirty.templatetags.tags import get_likes_count
import json
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User




class MainView(generic.ListView):
    model = Post
    template_name = "main.html"
    context_object_name = "list_popular_posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all()

class PopularView(generic.ListView):
    model = Post
    template_name = "popularposts.html"
    context_object_name = "list_popular_posts"
    paginate_by = 10

    def get_queryset(self):
        return Like.popular_posts.all()

class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = DirtyUserForm

    def post(self, request, *args, **kwargs):
        form = DirtyUserForm(request.POST, request=request)
        if form.is_valid():
            user = form.save(commit=False)
            karma_inited.send(sender=user)
            user.save()
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



def like_the_post(request, post_id):
    if request.user.is_authenticated():
        if request.method == "POST" and request.is_ajax() and request.user.is_authenticated():
            like_int = 1 if request.POST['submit'] == '+' else -1
            post = get_object_or_404(Post, pk=post_id)
            post_likes, created = post.likes.get_or_create(user=request.user)
            if created:
                post_likes.like = like_int
                post_liked.send(sender=post)
                post_likes.save()
                return HttpResponse(get_likes_count(post_id))
            if post_likes:
                if post_likes.like != like_int:
                    post_likes.like = like_int
                    post_liked.send(sender=post)
                    post_likes.save()
                    return HttpResponse(get_likes_count(post_id))
                else:
                    post_likes.like = 0
                    post_liked.send(sender=post)
                    post_likes.save()
                    return HttpResponse(get_likes_count(post_id))
            else:
                new_like = Like(user=request.user, post=post, like=like_int)
                post_liked.send(sender=post)
                new_like.save()
                return HttpResponse(get_likes_count(post_id))
    else:
        return HttpResponse("not_logged_in")




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


def defineOperator(karma, operator):
    if karma is not -2 and karma is not 2:
        return True

    op = '+' if karma == -2 else ''

    if karma == 2:
        op = '-'
    print(operator, ' ', op)
    return operator == op


def karma_edit(request, profile_name):
    if request.method == "POST" and request.is_ajax():
        karma_type = 1 if request.POST.get('karma_type') == '+' else -1
        user = get_object_or_404(DirtyUser, username=profile_name)
        #Init or get karma object

        vote_info, created = KarmaWVL.objects.get_or_create(who_added=request.user)
        if created:#Do work if only created or in range of karma
            user.karma.voted_users.add(vote_info)
            user.karma.count += karma_type
            vote_info.count += karma_type
            user.karma.save()
            vote_info.save()
            return HttpResponse(user.karma.count)
        else:
            if defineOperator(vote_info.count, request.POST.get('karma_type')):
                user.karma.count += karma_type
                vote_info.count += karma_type
                user.karma.save()
                vote_info.save()
                return HttpResponse(user.karma.count)
            else:
                return HttpResponse("error")

        #return HttpResponse(json.dumps({'karma': user.karma.count}), content_type="application/json")

class ProfileView(LoginRequiredMixin, View):

    def get(self, request, profile_name):
        user = get_object_or_404(DirtyUser, username=profile_name)
        isOwn = False
        if request.user.username == user.username:
            isOwn = True
        return render_to_response("profile.html", {'u': user, 'isOwn': isOwn, 'karma': user.karma.count}, context_instance=RequestContext(request))


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
    new_comment = Comment(post=comment.post, parent=comment, author=request.user, text=comment_text, isNotChild=False, head=comment.head+1)
    new_comment.save()
    return HttpResponseRedirect(reverse("post_view", args=(comment.post.id, )))

class ChangePassword(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        return render_to_response('change_password.html', {}, context_instance=RequestContext(request))

    def post(self, request):
        postdata = request.POST.copy()
        oldpassword = postdata['oldpassword']
        newpassword = postdata['newpassword']
        newpassword_repeat = postdata['newpassword_repeat']
        if request.user.check_password(oldpassword[0]):
            return render_to_response("change_password.html", {'errors': 'Неверно ввели старый пароль!'}, context_instance=RequestContext(request))
        if newpassword != newpassword_repeat:
            return render_to_response("change_password.html", {'errors': 'Введённые пароли не совпадают!'}, context_instance=RequestContext(request))
        request.user.set_password(newpassword)
        request.user.save()
        return HttpResponseRedirect(reverse('login_view'))

def add_favorite(request, post_id):
    if request.method == "POST" and request.is_ajax():
        favorite, create = Favorites.objects.get_or_create(post=Post.objects.get(pk=post_id), user=request.user)
        if create:
            favorite.save()
            return HttpResponse("OK!")
        else:
            return HttpResponse("error")
    else:
        return HttpResponse("check for some shit for tasties")


class FavoriteListView(generic.ListView):
    model = Post
    paginate_by = 10
    context_object_name = "list_of_favorites"

    # def get_queryset(self):
    #     return Favorites.objects.filter(user=self.request.user, )
