from django.shortcuts import redirect
from social.pipeline.partial import partial
from auth.utils import get_user_type, get_profile
from auth.models import PROFILE_CLASS
 
@partial
def get_username(strategy, details, user=None, is_new=False, *args, **kwargs):
    if is_new and details.get('email'):
        final_username = "%s_%s" % (get_user_type(), details.get("email"))
        return {'username': final_username}

def facebook_gender(strategy, details, user, is_new, *args, **kwargs):
    if details.get("gender"):
        try:
            profile = get_profile(user)
        except:
            gender = details.get("gender")[0].upper()
            profile = PROFILE_CLASS(user=user, gender = gender).save()

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            strategy.backend.REQUIRES_EMAIL_VALIDATION = True
            return redirect('require_email')
    return details
