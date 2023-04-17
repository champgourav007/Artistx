
def get_logged_user(request):
    if request.user.is_authenticated:
        return request.user
    else:
        return None