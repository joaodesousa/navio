from django.contrib.auth.models import User

def userData(request):  
    if request.user.is_authenticated:
        user = request.user
        us = User.objects.get(username=user)
        return {
            'us': us
        }
    return {}