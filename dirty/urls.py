from django.conf.urls import patterns, url, include
from dirty import views
from dirty.receivers import receiver


urlpatterns = patterns('',
    url(r'^$', views.MainView.as_view(), name='main_view'),
    url(r'^accounts/registration/$', views.RegisterView.as_view(), name='register_view'),
    url(r'^login/$', views.LoginView.as_view(), name='login_view'),
    url(r'^like/(?P<post_id>\d+)', views.like_the_post, name='like_view'),
    url(r'^logout/$', views.logout_view, name="logout_view"),
    url(r'^newpost/$', views.NewPost.as_view(), name='newpost_view'),
    url(r'^profile/(?P<profile_name>[a-zA-Z1-9]+)/$', views.ProfileView.as_view(), name='profile_view'),
    url(r'^comments/answer/(?P<comment_id>\d+)/$', views.answer_comment, name="comment_answer_view"),
    url(r'^profile/my/details/$', views.ProfileEdit.as_view(), name='profile_edit_view'),
    url(r'^profile/my/amnesia/$', views.ChangePassword.as_view(), name="password_edit_view"),
    url(r'karma/edit/(?P<profile_name>[a-zA-Z1-9]+)', views.karma_edit, name="karma_edit_view"),
    url(r'^comments/(?P<post_id>\d+)', views.PostView.as_view(), name="post_view"),
    url(r'^accounts/', include('registration.backends.default.urls')),

)
