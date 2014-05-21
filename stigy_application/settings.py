"""
Django settings for stigy_application project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5g2o5kc+d55z40%a+)#_qu47cj3))058)lpf&y$)#*fc2^4ig$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth',
    'registration',
    'registration_defaults',
    'social.apps.django_app.default',
    'bootstrap3'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auth.middleware.UpdateProfileMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware'
)

ROOT_URLCONF = 'stigy_application.urls'

WSGI_APPLICATION = 'stigy_application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

from registration_defaults.settings import *

USER_TYPE = "Customer"
LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_LOGIN_ERROR_URL = "/"

AUTHENTICATION_BACKENDS = (
      'social.backends.facebook.FacebookOAuth2',
      'social.backends.yahoo.YahooOpenId',
      'django.contrib.auth.backends.ModelBackend',
  )
SOCIAL_AUTH_FACEBOOK_KEY = '1426966484238395'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b39dc5690b46a00204d083ffafaccbce'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email', 'user_birthday', 'publish_stream']

SOCIAL_AUTH_YAHOO_FORCE_EMAIL_VALIDATION = True
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'auth.utils.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = "/email-sent/"

TEMPLATE_CONTEXT_PROCESSORS =  (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'auth.pipeline.require_email',
    'auth.pipeline.get_username',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'auth.pipeline.facebook_gender',
)

