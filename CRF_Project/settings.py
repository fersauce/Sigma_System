"""
Django settings for CRF_Project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4$!b$blxv(57$mbqfr2fnrjxf!y@1+=1#7a#hn@jwad*rixejt'

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
    'django_evolution',
    'Sigma_System',
    'south',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CRF_Project.urls'
ROOT_ARCHIVOS = os.path.join(PROJECT_PATH, 'archivos')
WSGI_APPLICATION = 'CRF_Project.wsgi.application'

ADMINS = (
    ('Fernando Saucedo', 'carlifer.fernando@gmail.com'),
    ('Cristian Candia', 'kandia88@gmail.com'),
    ('Ruth Centurion', 'ruthiccr@gmail.com'),
)
"""Administradores"""
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ss_des',
        'USER': 'sigmasystem',
        'PASSWORD': 'SS_is2.',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""Configuracion de la BD del sistema, ahora mismo en desarrollo"""

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-py'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_PROFILE_MODULE = 'Sigma_System.Usuario'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sigmasystem21@gmail.com'
EMAIL_HOST_PASSWORD = 'useruser'
EMAIL_PORT = 587
"""Configuracion del servidor de correo de la aplicacion"""

TEMPLATE_CONTEX_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',)