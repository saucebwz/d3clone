from django import forms
from django.contrib.auth.models import User
from dirty.models import Post, Comment
from registration.models import RegistrationProfile
from registration.forms import RegistrationForm
from dirty.models import DirtyUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from d3clone import settings
from django.contrib.sites.shortcuts import get_current_site


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description')


class CommentForm(forms.ModelForm):
    text = forms.CharField(min_length=1, widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = ('text', )



"""
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )
"""



class DirtyUserProfileForm(forms.ModelForm):
    #born = forms.DateField(input_formats=['%Y-%m-%d',      # '2006-10-25'
    #                                      '%m/%d/%Y',       # '10/25/2006'
    #                                      '%m/%d/%y'])

    about = forms.CharField(label="Информация о себе", widget=forms.Textarea)

    class Meta:
        model = DirtyUser
        fields = ('username', 'email', 'first_name', 'second_name', 'about')


class DirtyUserForm(forms.ModelForm):
    username = forms.CharField(label="Имя пользователя")
    email = forms.EmailField(label="Почта")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Имя")
    second_name = forms.CharField(label="Фамилия")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DirtyUserForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = DirtyUser
        fields = ('username', 'email', 'first_name', 'second_name', )

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords not match!")
        return password2

    def save(self, commit=True):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password2'],
                                                                    email=self.cleaned_data['email'],
                                                                    site=get_current_site(self.request))
        new_user.first_name = self.cleaned_data['first_name']
        new_user.second_name = self.cleaned_data['second_name']
        if commit:
            new_user.save()
        return new_user


class DirtyChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label="username", max_length=30, regex=r"^[\w.@+-]+$",
        help_text="Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."})

    password = ReadOnlyPasswordHashField(label="password",
        help_text="Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DirtyChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]