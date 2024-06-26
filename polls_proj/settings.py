"""
Django settings for polls_proj project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""







import os
from pathlib import Path


# https://pypi.org/project/dj-database-url/
import dj_database_url


# https://pypi.org/project/python-dotenv/
# https://github.com/theskumar/python-dotenv
#from dotenv import load_dotenv

#load_dotenv()  # take environment variables from .env.
# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.


# https://pypi.org/project/environs/#install
from environs import Env  # read .env file, if it exists
env = Env()
Env.read_env()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['polls-dev-zqte.2.us-1.fl0.io','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # my app
    'users.apps.UsersConfig',
    'polls.apps.PollsConfig',
    'pages.apps.PagesConfig',
    
    # built-in app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    # packages
    # https://pypi.org/project/crispy-bootstrap5/
    "crispy_forms",
    "crispy_bootstrap5",  
    
    # https://django-tinymce.readthedocs.io/en/latest/
    # https://pypi.org/project/django-tinymce/
    'tinymce',
    
    
    "django.contrib.sites",     # sitemaps
    'django.contrib.sitemaps',  # sitemaps 
     
]
# https://pypi.org/project/crispy-bootstrap5/
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # https://whitenoise.readthedocs.io/en/stable/index.html
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'polls_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],       # or you can write only    'DIRS':[BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'polls_proj.wsgi.application'



CSRF_TRUSTED_ORIGINS = ['https://polls-dev-zqte.2.us-1.fl0.io']

INTERNAL_IPS = (
    '127.0.0.1',
    'localhost:8000'
)





# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

#DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}




DATABASES = {
 #Development
    'default': {
         'ENGINE'  : 'django.db.backends.postgresql_psycopg2',

         'NAME'    : os.getenv('DB_NAME'),

         'USER'    :  os.getenv('DB_USER'),

         'PASSWORD':  os.getenv('DB_PASSWORD'),

         'HOST'    : os.getenv('DB_HOST'),

         'PORT'    : os.getenv('DB_PORT') ,
     }
 }
print(DATABASES)





#https://django-environ.readthedocs.io/en/latest/quickstart.html
# https://pypi.org/project/python-dotenv/
# https://github.com/theskumar/python-dotenv
#from dotenv import load_dotenv

#load_dotenv()  # take environment variables from .env.
# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
# DATABASES = {
#    'default':dj_database_url.parse(os.getenv("DATABASE_URL"),conn_max_age=600,conn_health_checks=True)
# }




 
# DATABASES = {
# PRODUCTION
#     'default': dj_database_url.parse('postgres://...',conn_max_age=600,conn_health_checks=True)
# }
# DATABASES = {
#    'default': dj_database_url.parse(env('DATABASE_URL'), conn_max_age=600, conn_health_checks=True)
# }

# print(DATABASES)




SITE_URL = 'https://polls-z0im.onrender.com/'

SITE_ID = 1  # sitemap - we have only one site in our project, we can use 1.


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



############################### STATIC ##################################
# Static files (CSS, JavaScript, Images)

# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
# https://whitenoise.readthedocs.io/en/latest/
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


STATICFILES_DIRS = [ BASE_DIR/"static"]  #for static folder than put in main project root(near mnage.py file),which contain static belong to all project
#STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),)     also work ok

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles') # for collectstatic for deployment

############################### MEDIA ##################################
# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/')                            # default storage of media in development 



# https://whitenoise.readthedocs.io/en/stable/index.html
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




############################################# messages.ERROR ##############################################
# https://docs.djangoproject.com/en/4.2/ref/contrib/messages/
# https://stackoverflow.com/questions/55202684/does-bootstrap-django-error-message-has-no-red-color
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}




############################### AUTH_USER_MODEL ##################################
AUTH_USER_MODEL = "users.CustomUser"




############################################# EMAIL settings ##############################################
# https://www.abstractapi.com/guides/django-send-email
# At this stage, we are going to configure email backend to send confirmation links. that done by tow ways:

# 1) to send confirmation links in console:
# -----------------------------------------
# EMAIL_BACKEND      = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'noreply@CodesCity'


#2) to send confirmation links by using your - SMTP Server of your Gmail or yahoo mail :
############# send email using  SMTP Gmail ########################
# -------------------------------------------------------------------
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'your_username@gmail.com'
# EMAIL_HOST_PASSWORD = 'yourpassword'         #Note: get 'yourpassword' from  #https://myaccount.google.com/apppasswords
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = 'noreply@yourwebsitename'



EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')        #Note: get 'yourpassword' from  #https://myaccount.google.com/apppasswords
EMAIL_PORT = env('EMAIL_PORT') 
EMAIL_USE_TLS = env('EMAIL_USE_TLS') 
# EMAIL_USE_SSL = env('EMAIL_USE_SSL')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# print(EMAIL_BACKEND)
# print(EMAIL_HOST)
# print(EMAIL_HOST_USER)
# print(EMAIL_HOST_PASSWORD)
# print(EMAIL_PORT)
# print(EMAIL_USE_TLS)
# print(DEFAULT_FROM_EMAIL)


# EMAIL_BACKEND = 'django_email_utils.backends.HTMLEmailBackend'
# EMAIL_HOST = 'smtp.your-smtp-server.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@example.com'
# EMAIL_HOST_PASSWORD = 'your_password'

# Debug logging (enable temporarily)
#logging.basicConfig(level=logging.DEBUG)




# EMAIL_BACKEND       = os.getenv('EMAIL_BACKEND')
# EMAIL_HOST          = os.getenv('EMAIL_HOST')
# EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_PORT          = os.getenv('EMAIL_PORT')
# EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS')
# #EMAIL_USE_SSL      = os.getenv('EMAIL_USE_SSL')
# DEFAULT_FROM_EMAIL  = os.getenv('DEFAULT_FROM_EMAIL')

# EMAIL_DEBUG = True
# if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
#     raise ValueError('Missing EMAIL_HOST_USER or EMAIL_HOST_PASSWORD in environment variables.')
 
 
 
LOGIN_URL = 'users:user-login'
