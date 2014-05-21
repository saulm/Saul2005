from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

def get_user_type():
    return "B" if settings.USER_TYPE == "Business" else "C"

def get_profile(user):
    return user.business_profile if get_user_type() == "B" else user.customer_profile


def send_validation(strategy, code):
    url = reverse('social:complete', args=(strategy.backend.name,)) + \
            '?verification_code=' + code.code
    send_mail('Validate your account',
              'Validate your account {0}'.format("http://localhost:8000"+url),
              settings.DEFAULT_FROM_EMAIL,
              [code.email],
              fail_silently=False)
