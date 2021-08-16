from .models import Profile

def avatar(request) :
    try :
        if request.user.is_authenticated :
            profile = Profile.objects.get(user=request.user)
            return {
                'avatar' : profile.avatar
            }
        else :
            return {
                'avatar' : Profile.objects.none()
            }
    except :
        return {
                'avatar' : Profile.objects.none()
            }