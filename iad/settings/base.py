"""
Django settings for iad project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, '../'))))

# Application definition

INSTALLED_APPS = [
    'dal',
    'django.contrib.admin',
    'dal_select2',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'crispy_forms',
    'django_filters',
    'django_tables2',
    'rest_framework',
    'rest_framework_gis',
    'reversion',
    'leaflet',
    'idprovider',
    'webpage',
    'vocabs',
    'entities',
    'bib',
    'sparql',
    'stats',
    'browsing',
    'arche',
    'archiv',
    'checks',
    'shapes',
    'charts',
]

CRISPY_TEMPLATE_PACK = "bootstrap3"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'iad.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webpage.webpage_content_processors.installed_apps',
                'webpage.webpage_content_processors.is_dev_version',
            ],
        },
    },
]

WSGI_APPLICATION = 'iad.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

ARCHE_SETTINGS = {
    'project_name': ROOT_URLCONF.split('.')[0],
    'base_url': "https://id.acdh.oeaw.ac.at/{}".format(ROOT_URLCONF.split('.')[0])
}

VOCABS_DEFAULT_PEFIX = os.path.basename(BASE_DIR)

VOCABS_SETTINGS = {
    'default_prefix': VOCABS_DEFAULT_PEFIX,
    'default_ns': "http://www.vocabs/{}/".format(VOCABS_DEFAULT_PEFIX),
    'default_lang': "eng"
}

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (47, 16),
    'DEFAULT_ZOOM': 6,
    'MIN_ZOOM': 3,
    'OVERLAYS': [
        (
            'World', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                'maxZoom': 25,
                'attribution':
                '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }
        ),
        (
            'Ortho World', 'https://api.mapbox.com/styles/v1/csae8092/cjj5eznid0gpu2sqau1eqiqr3/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiY3NhZTgwOTIiLCJhIjoiY2lnM2FoZWpjMDJqZnY1a2gxdWl6a29kaiJ9.FQXlsKIu60WhiXLrfI59VA',
            {
                'maxZoom': 25,
                'attribution': 'MapBox'
            }
        )
    ]
}
