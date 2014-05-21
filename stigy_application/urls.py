from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from django.contrib import admin
from django.contrib.auth.views import login
from auth.forms import UserRegistrationForm, LoginForm
from auth.views import edit_user_profile, require_email, validation_sent, home
from auth.utils import get_user_type

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', home, name="home"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^email/$', require_email, name='require_email'),
                       url(r'^email-sent/', validation_sent),
                       url(r'^accounts/register/$', RegistrationView.as_view(form_class=UserRegistrationForm), name='registration_register'),
                       url(r'^accounts/login/$', login, {'authentication_form': LoginForm}),
                       url(r'^accounts/profile/edit/$', edit_user_profile, name='edit_user_profile'),
                       (r'^accounts/', include('registration.backends.default.urls')),
)

if get_user_type() == "C":
    urlpatterns.append(url('^accounts/', include('social.apps.django_app.urls', namespace='social')))
