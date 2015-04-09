from dirty.models import Like


def username(request):
    if request.user.is_authenticated():
        return {'user': request.user}
    else:
        return {'user': 'None'}


