from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from auth.utils import get_profile, get_user_type

class UpdateProfileMiddleware(object):
    def process_request(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return
        ignore = [reverse('edit_user_profile'), reverse("auth_logout")]
        if request.user.is_authenticated() and not request.path in ignore:
            try:
                request.user_profile = get_profile(request.user)
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('edit_user_profile'))
                            
            if get_user_type() == "C" and  (request.user_profile.first_name == "" or request.user_profile.last_name == ""):
                return HttpResponseRedirect(reverse('edit_user_profile'))
            
