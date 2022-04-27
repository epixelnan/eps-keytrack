# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

# SECURITY: see https://docs.djangoproject.com/en/4.0/topics/security/#host-headers-virtual-hosting
ALLOWED_HOSTS = ['keytrack.epixel.in']

EPS_EMAIL_ENABLED = False
EPS_EMAIL_FROM = 'Epixel Keytrack <support@epixelmlmsystem.com>'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Recipient
EPS_EMAIL_OK_DOMAINS = ['epixelsolutions.com']

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
