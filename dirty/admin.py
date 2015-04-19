from django.contrib import admin
from dirty.models import Post, Comment, Like, DirtyUser, Karma
from dirty.forms import DirtyChangeForm, DirtyUserForm
from django.contrib.auth.admin import UserAdmin



class LikeInline(admin.TabularInline):
    model = Like
    extra = 10


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 10
    fieldsets = [
        ('Информация об лайках: ', {'fields': ['author', 'post'], 'classes': ['collapse']})
    ]


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Информация о посте', {'fields': ['user', 'title', 'description', 'is_gold']}),
    ]
    list_display = ('user', 'title', 'description', 'created_on')
    search_fields = ['user, title']
    inlines = [CommentInline, LikeInline]


class ProfileAdmin(admin.ModelAdmin):
    fields = ('about', 'born')
    search_fields = ('about', 'born')
    list_display = ('about', 'born')

class DirtyUserAdmin(UserAdmin):
    form = DirtyChangeForm
    add_form = DirtyUserForm
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'second_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    list_display = ('email', )
    list_filter = ('is_active', )
    search_fields = ('first_name', 'second_name', 'email')
    ordering = ('email',)


admin.site.register(Post, PostAdmin)
admin.site.register(DirtyUser, DirtyUserAdmin)
admin.site.register(Karma)
#admin.site.register(Profile, ProfileAdmin)